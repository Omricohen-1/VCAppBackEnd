from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
THRESHOLD = 21  # days
user = "noreply@hebits.net"


def authentication():
    """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=81)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def create_threshold_date(threshold):
    """calculates the date 'threshold' days ago, and returns it as String"""
    today_date = datetime.datetime.today().date()
    threshold_diff = datetime.timedelta(days=threshold)
    threshold_date = today_date - threshold_diff
    return f"{threshold_date.year}/{threshold_date.month}/{threshold_date.day}"


def bring_all_mess(service):
    """returns all the mails in your Gmail account from the last day"""
    threshold_date = create_threshold_date(1)
    allMes = service.users().messages().list(userId='me', q=f"after:{threshold_date}").execute()
    for mess in allMes['messages']:
        messId = mess['id']
        message = service.users().messages().get(userId='me', id=messId).execute()
        print(message)


def bring_filtered_mess(service, user, threshold):
    """returns all the mails in your Gmail account sent by user sent in the last 'threshold' days"""
    threshold_date = create_threshold_date(threshold)
    allMes = service.users().messages().list(userId='me', q=f"from:{user}, after:{threshold_date}").execute()
    for mess in allMes['messages']:
        messId = mess['id']
        message = service.users().messages().get(userId='me', id=messId).execute()
        print(message)


def main():
    service = authentication()
    bring_all_mess(service)


if __name__ == '__main__':
    main()
