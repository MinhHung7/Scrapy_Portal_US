import datetime
import os.path

from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def event_exists(service, calendar_id, event_data):
    events = service.events().list(
        calendarId=calendar_id,
        timeMin=event_data["start"]["dateTime"],
        timeMax=event_data["end"]["dateTime"],
        singleEvents=True,
    ).execute()
    return "items" in events and len(events["items"]) > 0

def main(event_list, summary):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        calendar_id = summary  # Set your desired calendar ID

        # Check if the calendar exists
        calendars = service.calendarList().list().execute()
        calendar_exists = any(calendar["summary"] == calendar_id for calendar in calendars.get("items", []))

        # If the calendar doesn't exist, create it
        if not calendar_exists:
            calendar_body = {
                "summary": summary,
                "timeZone": "Asia/Ho_Chi_Minh",  # Specify your desired time zone
            }
            created_calendar = service.calendars().insert(body=calendar_body).execute()
            calendar_id = created_calendar["id"]
        else:
            # Calendar exists, get its ID
            calendar_id = next((calendar["id"] for calendar in calendars.get("items", []) if calendar["summary"] == summary), None)
        
        event_list_calendar = []
        for event in event_list:
            event_create = {
                "summary": event.header,
                "location": event.content,
                "description": event.content,
                "colorID": 6,
                "start": {
                    "dateTime": event.date + "T" + event.start_time + "+07:00",
                    "timeZone": "Asia/Ho_Chi_Minh"
                },
                "end": {
                    "dateTime": event.date + "T" + event.end_time + "+07:00",
                    "timeZone": "Asia/Ho_Chi_Minh"
                },
                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {"method": "popup", "minutes": 24 * 60},  # 1 day before
                    ],
                },
                "recurrence": [
                    "RRULE:FREQ=DAILY;COUNT=1"
                ],
            }
            if not event_exists(service, calendar_id, event_create):
                event_list_calendar.append(event_create)

        for event_data in event_list_calendar:
            event = service.events().insert(calendarId=calendar_id, body=event_data).execute()

    except HttpError as error:
        print(f"An error occurred: {error}")
