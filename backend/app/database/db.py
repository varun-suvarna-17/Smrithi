import uuid
import logging
from typing import Dict, List, Optional, Any

from app.utils.helpers import utc_now_iso

logger = logging.getLogger("smrithi.database")


class InMemoryCollection:
    """
    Simple in-memory collection used for local development and testing.

    This temporarily replaces the production Firebase database.
    Data will be lost when the backend is restarted.
    """

    def __init__(self, name: str):
        self.name = name
        self.documents: Dict[str, dict] = {}

    def insert_one(self, doc: dict) -> dict:
        doc = dict(doc)

        if "_id" not in doc:
            doc["_id"] = str(uuid.uuid4())

        if "id" not in doc:
            doc["id"] = doc["_id"]

        if "created_at" not in doc:
            doc["created_at"] = utc_now_iso()

        if "updated_at" not in doc:
            doc["updated_at"] = utc_now_iso()

        self.documents[str(doc["_id"])] = doc

        return dict(doc)

    def find_one(self, query: dict) -> Optional[dict]:
        for doc in self.documents.values():
            if self._matches(doc, query):
                return dict(doc)

        return None

    def find(
        self,
        query: Optional[dict] = None,
        sort_by: Optional[str] = None,
        reverse: bool = False,
        limit: Optional[int] = None
    ) -> List[dict]:

        query = query or {}

        results = [
            dict(doc)
            for doc in self.documents.values()
            if self._matches(doc, query)
        ]

        if sort_by:
            results.sort(
                key=lambda x: str(x.get(sort_by, "")),
                reverse=reverse
            )

        if limit is not None:
            results = results[:limit]

        return results

    def update_one(self, query: dict, update_data: dict) -> bool:
        doc = self.find_one(query)

        if not doc:
            return False

        doc_id = str(doc["_id"])

        if doc_id not in self.documents:
            return False

        target = self.documents[doc_id]

        # Support MongoDB-style $set syntax used by existing services.
        updates = update_data.get("$set", update_data)

        for key, value in updates.items():
            if not key.startswith("$"):
                target[key] = value

        target["updated_at"] = utc_now_iso()

        return True

    def delete_one(self, query: dict) -> bool:
        doc = self.find_one(query)

        if not doc:
            return False

        doc_id = str(doc["_id"])

        if doc_id in self.documents:
            del self.documents[doc_id]
            return True

        return False

    def count(self, query: Optional[dict] = None) -> int:
        return len(self.find(query))

    def _matches(self, doc: dict, query: dict) -> bool:
        for key, value in query.items():

            if key in ("_id", "id"):
                if (
                    str(doc.get("_id")) != str(value)
                    and str(doc.get("id")) != str(value)
                ):
                    return False

            elif doc.get(key) != value:
                return False

        return True


class DatabaseManager:
    """
    SMRITHI database manager.

    Current:
        In-memory database for local development and API testing.

    Future:
        Firebase/Firestore will be integrated here once the
        Firebase configuration and credentials are available.
    """

    def __init__(self):
        self.is_connected: bool = False
        self.mode: str = "in_memory"

        # Temporary local collections.
        self._collections: Dict[str, Any] = {}

    def connect(self):
        """
        Initialize the temporary in-memory database.

        Firebase will replace this implementation when the
        Firebase configuration is available.
        """

        self.mode = "in_memory"
        self.is_connected = True

        logger.info(
            "SMRITHI database initialized in In-Memory mode. "
            "Firebase integration is pending."
        )

    def get_collection(self, name: str):
        """
        Get or create an in-memory collection.
        """

        if name not in self._collections:
            self._collections[name] = InMemoryCollection(name)

        return self._collections[name]

    @property
    def users(self):
        return self.get_collection("users")

    @property
    def patients(self):
        return self.get_collection("patients")

    @property
    def caregivers(self):
        return self.get_collection("caregivers")

    @property
    def games(self):
        return self.get_collection("games")

    @property
    def game_attempts(self):
        return self.get_collection("game_attempts")

    @property
    def reminders(self):
        return self.get_collection("reminders")

    @property
    def reports(self):
        return self.get_collection("reports")

    @property
    def alerts(self):
        return self.get_collection("alerts")

    def reset_for_testing(self):
        """
        Clear all in-memory collections.

        Useful for tests.
        """

        self._collections = {}


# Global database manager used by the application.
db = DatabaseManager()