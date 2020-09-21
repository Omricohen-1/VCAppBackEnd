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
# user = "noreply@hebits.net"


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


# global variable
service = authentication()


#TODO: change to ISO timestamp
def fix_time_display(date):
    date_split = date.split()
    time_split = date_split[4].split(':')
    iso_time = datetime.datetime.strptime(f'{date_split[3]}-{date_split[2]}-{date_split[1]} {time_split[0]}:{time_split[1]}:{time_split[2]}', '%Y-%b-%d %H:%M:%S')
    return str(iso_time)


def fix_contact_display(contact):
    array = contact.split()
    return array[1][1:-1]


def get_value(message):
    """receives dict with message's info and returns the date it was sent and participant"""
    for item in message['payload']['headers']:
        if item['name'] == 'From':
            contact = fix_contact_display(item['value'])
        if item['name'] == 'Date':
            date = fix_time_display(item['value'])
    return contact, date


def create_threshold_date(threshold):
    """calculates the date 'threshold' days ago, and returns it as String"""
    today_date = datetime.datetime.today().date()
    threshold_diff = datetime.timedelta(days=threshold)
    threshold_date = today_date - threshold_diff
    return f"{threshold_date.year}/{threshold_date.month}/{threshold_date.day}"


def bring_all_mess():
    """returns all the mails in your Gmail account"""
    all_messages = service.users().messages().list(userId='me', q=f"after:2015/01/01").execute()
    return all_messages


def bring_all_mess_from_yesterday():
    """returns all the mails in your Gmail account from the last day"""
    threshold_date = create_threshold_date(3)
    all_messages = service.users().messages().list(userId='me', q=f"after:{threshold_date}").execute()
    return all_messages


def bring_filtered_mess(contact, threshold):
    """returns all the mails in your Gmail account sent by user sent in the last 'threshold' days
    :parameter service: gives access to your gmail account
    :parameter contact: the sender e-mail account 'user@example.com'
    :parameter threshold: number of days back to search for
    """
    threshold_date = create_threshold_date(threshold)
    all_messages = service.users().messages().list(userId='me', q=f"from:{contact}, after:{threshold_date}").execute()
    return all_messages


def create_contact_date_array(all_messages):
    contact_date_array = []
    for mess in all_messages['messages']:
        messId = mess['id']
        message = service.users().messages().get(userId='me', id=messId).execute()
        print(get_value(message))
        contact_date_array.append(get_value(message))
    return contact_date_array


def main():
    allMes = bring_all_mess_from_yesterday()
    create_contact_date_array(allMes)


if __name__ == '__main__':
    main()

# returns a list of all the mails the contact had: mail of sender, date


# def find_latest_message(allMes):
#     latest = datetime.datetime(2000, 1, 1).date()
#     for mess in allMes['messages']:
#         messId = mess['id']
#         message = service.users().messages().get(userId='me', id=messId).execute()
#         print(message)
#         mess_date = export_date_from_message(message)
#         if mess_date > latest:
#             latest = mess_date
#     return latest