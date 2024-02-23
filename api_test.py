import os.path
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# when scopes is modified, delete token.json and reauthorize
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events.readonly",
]


def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        with build("oauth2", "v2", credentials=creds) as service:
            user_info = service.userinfo().get().execute()
            print(user_info)

        service = build("calendar", "v3", credentials=creds)
        print("List calendars")
        page_token = None
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list["items"]:
                print(calendar_list_entry["summary"])
            page_token = calendar_list.get("nextPageToken")
            if not page_token:
                break

        # Retrieve last month's
        current_time = datetime.datetime.now()
        last_month = current_time - datetime.timedelta(days=30)
        last_month = last_month.isoformat() + "Z"

        page_token = None
        counts = 0
        while counts < 10:  # limit to 10 pages max
            counts += 1
            events = (
                service.events()
                .list(calendarId="primary", pageToken=page_token, timeMin=last_month)
                .execute()
            )
            for event in events["items"]:
                if event["status"] == "cancelled":
                    continue
                missing_fields = False
                if "summary" not in event:
                    event["summary"] = "Untitled"
                    missing_fields = True
                print(event["summary"])
                if "start" not in event:
                    print("No start time")
                    missing_fields = True
                else:
                    print("\t" + event["start"]["dateTime"])
                if "end" not in event:
                    print("No end time")
                    missing_fields = True
                else:
                    print("\t" + event["end"]["dateTime"])
                if missing_fields:
                    print(event)
            page_token = events.get("nextPageToken")
            if not page_token:
                break
    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()
