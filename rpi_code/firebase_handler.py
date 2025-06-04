import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import uuid
from typing import Optional, Dict, Any

cred = credentials.Certificate("sortimate_firebase_key.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

def log_waste_event(
    bin_id: str,
    waste_type: str,
    raw_image_path: Optional[str] = None,
    user_id: Optional[str] = None,
    is_error: bool = False,
    error_message: Optional[str] = None,
    latency_ms: Optional[int] = None,
    confidence: Optional[float] = None
) -> None:
    """
    Log a waste event to the 'waste_events' collection.
    """
    event_id = str(uuid.uuid4())
    event_data: Dict[str, Any] = {
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
    try:
        db.collection("waste_events").document(event_id).set(event_data)
    except Exception as e:
        print(f"Failed to log waste event: {e}")

def update_bin_status(
    bin_id: str,
    location: Optional[str] = None,
    alerts: Optional[Dict[str, bool]] = None,
    capacity: Optional[Dict[str, Any]] = None,
    notes: Optional[str] = None
) -> None:
    """
    Update the status of a bin in the 'bins' collection.
    """
    bin_ref = db.collection("bins").document(bin_id)
    updates: Dict[str, Any] = {
        "last_update": datetime.datetime.now()
    }
    if location:
        updates["location"] = location
    if alerts:
        updates["alerts"] = alerts
    if capacity:
        updates["capacity"] = capacity
    if notes:
        updates["notes"] = notes
    try:
        bin_ref.set(updates, merge=True)
    except Exception as e:
        print(f"Failed to update bin status: {e}")

def create_alert(
    bin_id: str,
    message: str,
    alert_type: str,
    resolved: bool = False
) -> None:
    """
    Create an alert in the 'alerts' collection.
    """
    alert_data = {
        "bin_id": bin_id,
        "created_at": datetime.datetime.now(),
        "message": message,
        "resolved": resolved,
        "type": alert_type
    }
    try:
        db.collection("alerts").add(alert_data)
    except Exception as e:
        print(f"Failed to create alert: {e}")

if __name__ == "__main__":
    log_waste_event(bin_id="bin_001",waste_type="plastic",user_id="20994208",latency_ms=500, confidence=0.5)



