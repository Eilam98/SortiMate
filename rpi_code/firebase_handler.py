import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import uuid

cred = credentials.Certificate("sortimate_firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def log_waste_event(bin_id, waste_type, raw_image_path=None, user_id=None,
                    is_error=False, error_message=None, latency_ms=None, confidence=None):
    event_id = str(uuid.uuid4())
    event_data = {
        "event_id": event_id,
        "bin_id": bin_id,
        "timestamp": datetime.datetime.now(),
        "waste_type": waste_type,
        "raw_image_path": raw_image_path,
        "user_id": user_id,
        "is_error": is_error,
        "error_message": error_message,
        "latency_ms": latency_ms,
        "confidence": confidence
    }
    # Remove None values
    event_data = {k: v for k, v in event_data.items() if v is not None}
    db.collection("waste_events").document(event_id).set(event_data)


def update_bin_status(bin_id, alert_waste_type=None):
    bin_ref = db.collection("bins").document(bin_id)
    updates = {
        "last_update": datetime.datetime.now()
    }
    if alert_waste_type:
        updates["alerts." + alert_waste_type] = True
    bin_ref.set(updates, merge=True)


def create_alert(bin_id, message, alert_type):
    db.collection("alerts").add({
        "bin_id": bin_id,
        "created_at": datetime.datetime.now(),
        "message": message,
        "resolved": False,
        "type": alert_type
    })

if __name__ == "__main__":
    log_waste_event(bin_id="bin_001",waste_type="plastic",user_id="20994208",latency_ms=500, confidence=0.5)