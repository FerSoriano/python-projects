
import os
import json
import hashlib
import logging
import datetime
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, Tuple
from google.oauth2 import service_account
from googleapiclient.discovery import build
from .email_notifications import EmailNotification

logger = logging.getLogger(__name__)
email = EmailNotification()
load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CALENDAR_ID = os.getenv('CALENDAR_ID')
EVENT_INDEX_PATH = Path(__file__).resolve().parent.parent / "data" / "event_index.json"


class GoogleCalendarService():
    def __init__(self):
        self.service = self._authenticate()

    def _authenticate(self):
        key_path = os.getenv('GOOGLE_CALENDAR_SERVICE_ACCOUNT')
        if not key_path:
            raise ValueError("Error: La variable de entorno 'GOOGLE_CALENDAR_SERVICE_ACCOUNT' no está definida.")
        
        try:
            creds = service_account.Credentials.from_service_account_file(
                key_path, scopes=SCOPES
            )
            return build("calendar", "v3", credentials=creds)

        except Exception as error:
            error_message = "Error al autenticar la cuenta de servicio."
            logger.exception(error_message)
            email.sendFailedNotification(
                    subject=error_message,
                    body=str(error)
                )
            raise


class GoogleCalendarManager(GoogleCalendarService):
    def __init__(self):
        super().__init__()
        self.event_index = self._load_event_index()

    def _load_event_index(self):
        if not EVENT_INDEX_PATH.exists():
            return {}

        try:
            with EVENT_INDEX_PATH.open("r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return {}

    def _save_event_index(self):
        EVENT_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
        with EVENT_INDEX_PATH.open("w", encoding="utf-8") as file:
            json.dump(self.event_index, file, indent=2, ensure_ascii=False)

    def _build_event_key(self, event_name):
        raw_key = event_name.strip().lower()
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    def create_event(self, event_data, calendar_id):
        event = self.service.events().insert(
            calendarId=calendar_id,
            body=event_data
        ).execute()
        return event

    def update_event(self, event_data, calendar_id, event_id):
        event = self.service.events().update(
            calendarId=calendar_id,
            eventId=event_id,
            body=event_data
        ).execute()
        return event

    def get_event_by_id(self, calendar_id, event_id):
        try:
            return self.service.events().get(
                calendarId=calendar_id,
                eventId=event_id
            ).execute()
        except Exception:
            return None

    def find_event_by_summary(self, calendar_id, summary):
        events_result = self.service.events().list(
            calendarId=calendar_id,
            q=summary,
            timeMin="2000-01-01T00:00:00Z",
            singleEvents=True
        ).execute()
        events = events_result.get("items", [])

        for event in events:
            if event.get("summary") == summary:
                return event
        return None

    def get_event_by_hash(self, calendar_id, event_hash, summary=None):
        indexed_event = self.event_index.get(event_hash)
        if indexed_event:
            event = self.get_event_by_id(calendar_id, indexed_event.get("event_id"))
            if event:
                return event

        events_result = self.service.events().list(
            calendarId=calendar_id,
            privateExtendedProperty=f"event_hash={event_hash}",
            singleEvents=True
        ).execute()
        events = events_result.get('items', [])

        if not events:
            if summary:
                return self.find_event_by_summary(calendar_id, summary)
            return None

        event = events[0]
        self.event_index[event_hash] = {
            "event_id": event["id"],
            "summary": event.get("summary", "")
        }
        self._save_event_index()
        return event


    def add_event(self, event_name: str, due_date: str, notes: str) -> Tuple[bool, str]:
        event_created = False
        
        event_hash = self._build_event_key(event_name)

        start_date_obj = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
        end_date_obj = start_date_obj + datetime.timedelta(days=1)

        event_data = {
            "summary": event_name,
            "description": notes,
            "start": {
                "date": start_date_obj.strftime("%Y-%m-%d")
            },
            "end": {
                "date": end_date_obj.strftime("%Y-%m-%d")
            },
            "transparency": "transparent",
            "reminders": {
                "useDefault": False
            },
            "extendedProperties": {
                "private": {
                    "event_hash": event_hash
                }
            }
        }

        existing_event = self.get_event_by_hash(CALENDAR_ID, event_hash, event_name)

        if not existing_event:
            created_event = self.create_event(
                event_data=event_data,
                calendar_id=CALENDAR_ID
            )
            self.event_index[event_hash] = {
                "event_id": created_event["id"],
                "summary": event_name
            }
            self._save_event_index()
            logger.info("Nuevo evento: %s el dia %s", event_name, due_date)
            event_created = True
            msg = f"Tarea '{event_name}' creada con éxito para el dia: {due_date}"
        else:
            existing_start_date = existing_event.get("start", {}).get("date")
            existing_notes = existing_event.get("description", "")
            
            if existing_start_date == start_date_obj.strftime("%Y-%m-%d") and existing_notes == notes:
                event_created = False
                msg = f"Tarea '{event_name}' ya registrada y sin cambios para el dia: {due_date}"
            else:
                self.update_event(
                    event_data=event_data,
                    calendar_id=CALENDAR_ID,
                    event_id=existing_event["id"]
                )
                event_created = True
                msg = f"Tarea '{event_name}' actualizada con éxito para el dia: {due_date}"

        return event_created, msg
