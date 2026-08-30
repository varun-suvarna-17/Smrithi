import uuid
from typing import List, Dict, Any, Optional
from app.utils.helpers import utc_now_iso
from app.database.db import db
from app.schemas import ReminderCreate, ReminderUpdate

class ReminderService:
    @staticmethod
    def create_reminder(data: ReminderCreate) -> Dict[str, Any]:
        reminder_doc = {
            "id": f"rem_{uuid.uuid4().hex[:8]}",
            "patient_id": data.patient_id,
            "title": data.title,
            "message": data.message,
            "reminder_type": data.reminder_type.value,
            "scheduled_time": data.scheduled_time,
            "recurring": data.recurring,
            "frequency": data.frequency,
            "is_completed": False,
            "caregiver_id": data.caregiver_id,
            "created_at": utc_now_iso()
        }
        db.reminders.insert_one(reminder_doc)
        return reminder_doc

    @staticmethod
    def get_patient_reminders(patient_id: str, include_completed: bool = True) -> List[Dict[str, Any]]:
        query = {"patient_id": patient_id}
        if not include_completed:
            query["is_completed"] = False
        return db.reminders.find(query=query, sort_by="scheduled_time", reverse=False)

    @staticmethod
    def get_reminder(reminder_id: str) -> Optional[Dict[str, Any]]:
        return db.reminders.find_one({"id": reminder_id})

    @staticmethod
    def update_reminder(reminder_id: str, updates: ReminderUpdate) -> Optional[Dict[str, Any]]:
        clean_updates = {k: v for k, v in updates.model_dump(exclude_unset=True).items() if v is not None}
        if "reminder_type" in clean_updates:
            clean_updates["reminder_type"] = clean_updates["reminder_type"].value
        
        success = db.reminders.update_one({"id": reminder_id}, {"$set": clean_updates})
        if success:
            return db.reminders.find_one({"id": reminder_id})
        return None

    @staticmethod
    def delete_reminder(reminder_id: str) -> bool:
        return db.reminders.delete_one({"id": reminder_id})

    @staticmethod
    def mark_completed(reminder_id: str, completed: bool = True) -> Optional[Dict[str, Any]]:
        success = db.reminders.update_one({"id": reminder_id}, {"$set": {"is_completed": completed}})
        if success:
            return db.reminders.find_one({"id": reminder_id})
        return None
