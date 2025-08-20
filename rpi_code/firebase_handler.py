# firebase_handler.py
import os
import uuid

import firebase_admin
from firebase_admin import credentials, firestore as admin_fs
from google.api_core import retry as g_retry
from google.cloud.firestore_v1 import SERVER_TIMESTAMP
from google.cloud.firestore_v1 import FieldFilter

# ---- Helper retry (handles transient network hiccups on the RPi) ----
_WRITE_RETRY = g_retry.Retry(
    initial=0.2, maximum=5.0, multiplier=2.0, deadline=20.0,
    predicate=g_retry.if_exception_type(Exception)
)

class FirebaseHandler:
    def __init__(self, service_account_path="/home/pi/creds/sortimate_firebase_key.json", app_name="SortiMate"):
        """
        Initialize Firebase Admin SDK and Firestore client.

        If service_account_path is None, uses GOOGLE_APPLICATION_CREDENTIALS env var.
        """
        
        cred_obj = credentials.Certificate(service_account_path)

        # Initialize app once (safe on re-import or long-running processes)
        try:
            self.app = firebase_admin.get_app(app_name)
        except ValueError:
            self.app = firebase_admin.initialize_app(cred_obj, name=app_name)

        self.db = admin_fs.client(app=self.app)
        self._listeners = []  # keep references to stop them later

    # ---------- Basic create/update helpers ----------
    @_WRITE_RETRY
    def set_document(self, collection, doc_id, data, merge=True):
        filtered_data = {field_name: field_value for field_name, field_value in data.items() if field_value is not None}
        self.db.collection(collection).document(doc_id).set(filtered_data, merge=merge)

    @_WRITE_RETRY
    def add_document(self, collection, data):
        filtered_data = {field_name: field_value for field_name, field_value in data.items() if field_value is not None}
        doc_ref, _write_time = self.db.collection(collection).add(filtered_data)
        return doc_ref.id

    # ---------- Your domain methods ----------
    def log_waste_event(self, bin_id, waste_type, confidence=None):
        """
        Log a waste event to 'waste_events' (returns event_id).
        """
        event_id = str(uuid.uuid4())
        event_data = {
            "event_id": event_id,
            "bin_id": bin_id,
            "timestamp": SERVER_TIMESTAMP,
            "waste_type": waste_type,
            "confidence": confidence,
        }
        self.set_document("waste_events", event_id, event_data, merge=False)
        return event_id

    def log_wrong_classification(self, bin_id, real_classified_waste_type, confidence, image_cloudinary_url, user_answered=False):
        event_id = str(uuid.uuid4())
        event_data = {
            "event_id": event_id,
            "bin_id": bin_id,
            "timestamp": SERVER_TIMESTAMP,
            "model_classification_waste_type": real_classified_waste_type,
            "confidence": confidence,
            "image_cloudinary_url": image_cloudinary_url,
            "user_answered": user_answered,
            "user_classified_type": None,
            "reviewed": False
        }
        self.set_document("wrong_classifications", event_id, event_data, merge=False)
        return event_id

    def update_wrong_classification_user_answer(self, event_id, user_classified_type):
        """
        Update a wrong_classification document when user provides the correct waste type.
        Sets user_answered to True and stores the user's choice.
        """
        updates = {
            "user_answered": True,
            "user_classified_type": user_classified_type,
            "timestamp_user_answer": SERVER_TIMESTAMP
        }
        self.set_document("wrong_classifications", event_id, updates, merge=True)

    def update_bin_status(self, bin_id, status):
        """
        Upsert a bin in 'bins' with last_update set server-side.
        """
        updates = {
            "last_update": SERVER_TIMESTAMP,
            "status": status,
        }
        self.set_document("bins", bin_id, updates, merge=True)
    
    # ---------- Realtime listeners ----------
    def listen_to_collection(
        self,
        collection_path,
        on_added=None,
        on_modified=None,
        on_removed=None,
        filters=None,
    ):
        """
        Attach a realtime listener to a collection with optional simple filters.
        Each change will call the respective callback with the DocumentSnapshot.

        Returns a function to stop the listener.
        """
        query = self.db.collection(collection_path)
        if filters:
            for f in filters:
                if len(f) == 3:
                    field, op, value = f
                    filter_obj = FieldFilter(field, op, value)
                    query = query.where(filter=filter_obj)

        def _on_snapshot(col_snapshot, changes, read_time):
            # Robust: if callbacks error, don't kill the stream
            for change in changes:
                try:
                    if change.type.name == "ADDED" and on_added:
                        on_added(change.document)
                    elif change.type.name == "MODIFIED" and on_modified:
                        on_modified(change.document)
                    elif change.type.name == "REMOVED" and on_removed:
                        on_removed(change.document)
                except Exception as e:
                    print(f"[Listener error] {e}")

        watch = query.on_snapshot(_on_snapshot)
        self._listeners.append(watch)

        def stop():
            try:
                watch.unsubscribe()
                self._listeners.remove(watch)
            except Exception:
                pass

        return stop

    def stop_all_listeners(self):
        for w in list(self._listeners):
            try:
                w.unsubscribe()
            except Exception:
                pass
        self._listeners.clear()

    def listen_for_wrong_classification_answer(self, event_id, on_answered):
        """
        Start a listener for a single wrong_classifications item.
        Calls on_answered(doc_snapshot) once when user_answered becomes True.
        Returns a stop() function you must call to unsubscribe.
        """
        def _on_mod(doc):
            data = doc.to_dict() or {}
            if data.get("user_answered") is True:
                try:
                    on_answered(doc)   # let caller decide what to do
                finally:
                    # stop this one-shot stream after first answer
                    stop()

        stop = self.listen_to_collection(
            "wrong_classifications",
            on_modified=_on_mod,
            filters=[("event_id", "==", event_id)]
        )
        return stop