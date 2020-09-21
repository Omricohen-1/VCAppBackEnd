from __future__ import print_function
import json
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime

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
    if os.path.exists(r'token.pickle'):
        with open(r'token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'token.pickle', SCOPES)
            creds = flow.run_local_server(port=81)
        # Save the credentials for the next run
        with open(r'token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def export_date_from_message(message):
    """receives dict with message's info and returns the date it was sent"""
    time_message_sent = message['payload']['headers'][1]['value']
    array = time_message_sent.split()
    return datetime.datetime.strptime(f'{array[8]}-{array[7]}-{array[9]}', '%b-%d-%Y').date()


def create_threshold_date(threshold):
    """calculates the date 'threshold' days ago, and returns it as String"""
    today_date = datetime.datetime.today().date()
    threshold_diff = datetime.timedelta(days=threshold)
    threshold_date = today_date - threshold_diff
    return f"{threshold_date.year}/{threshold_date.month}/{threshold_date.day}"


def bring_all_mess(service):
    """returns all the mails in your Gmail account from the last day"""
    threshold_date = create_threshold_date(3)
    allMes = service.users().messages().list(userId='me', q=f"after:{threshold_date}").execute()
    return allMes


def bring_filtered_mess(service, user, threshold):
    """returns all the mails in your Gmail account sent by user sent in the last 'threshold' days
    :parameter service: gives access to your gmail account
    :parameter user: the sender e-mail account 'user@example.com'
    :parameter threshold: number of days back to search for
    """
    threshold_date = create_threshold_date(threshold)
    allMes = service.users().messages().list(userId='me', q=f"from:{user}, after:{threshold_date}").execute()
    return allMes


def find_latest_message(service, allMes):
    latest = datetime.datetime(2000, 1, 1).date()
    for mess in allMes['messages']:
        messId = mess['id']
        message = service.users().messages().get(userId='me', id=messId).execute()
        mess_date = export_date_from_message(message)
        if mess_date > latest:
            latest = mess_date
    return latest


def main():
    service = authentication()
    allMes = bring_all_mess(service)
    print(find_latest_message(service, allMes))


if __name__ == '__main__':
    main()
