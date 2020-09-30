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


def display_time_iso(date):
    date_split = date.split()
    time_split = date_split[4].split(':')
    iso_time = datetime.datetime.strptime(f'{date_split[3]}-{date_split[2]}-{date_split[1]} {time_split[0]}:{time_split[1]}:{time_split[2]}', '%Y-%b-%d %H:%M:%S')
    return str(iso_time)


def fix_contact_email_display(contact):
    """extract only the contact's email from the info in the message 'From' value"""
    array = contact.split()
    return array[1][1:-1]


#TODO: check sent items
def get_value(message):
    """receives dict with message's info and returns the date it was sent and contact email"""
    if message['id'] == "174b4fe943c402a4":
        print("")
    for item in message['payload']['headers']:
        # finds the receiver and sender of the mail, and chooses the email that is not our own
        if item['name'] == 'Delivered - To':
            contact = item['value']
            if contact == "my mail": #TODO: fix to user mail
                if item['name'] == 'From':
                    contact = fix_contact_email_display(item['value'])
        if item['name'] == 'Date':
            date = display_time_iso(item['value'])
    return contact, date


def create_threshold_date(threshold):
    """calculates the date 'threshold' days ago, and returns it as String"""
    today_date = datetime.datetime.today().date()
    threshold_diff = datetime.timedelta(days=threshold)
    threshold_date = today_date - threshold_diff
    return f"{threshold_date.year}/{threshold_date.month}/{threshold_date.day}"


def create_contact_date_array(all_messages):
    if all_messages['resultSizeEstimate'] == 0:
        return []
    contact_date_array = []
    for mess in all_messages['messages']:
        messId = mess['id']
        message = service.users().messages().get(userId='me', id=messId).execute()
        contact_date_array.append(get_value(message))
    return contact_date_array


def bring_all_mess():
    """returns all the mails in your Gmail account"""
    all_messages = service.users().messages().list(userId='me', q=f"after:2015/01/01").execute()
    return create_contact_date_array(all_messages)


def bring_all_mess_from_yesterday():
    """returns all the mails in your Gmail account from the last day"""
    threshold_date = create_threshold_date(3)
    all_messages = service.users().messages().list(userId='me', q=f"after:{threshold_date}").execute()
    return create_contact_date_array(all_messages)


def bring_filtered_mess(contact_email, threshold):
    """returns all the mails in your Gmail account sent by user sent in the last 'threshold' days
    :parameter contact_email: the sender e-mail account 'user@example.com'
    :parameter threshold: number of days back to search for
    """
    threshold_date = create_threshold_date(threshold)
    all_messages = service.users().messages().list(userId='me', q=f"from:{contact_email}, after:{threshold_date}").execute()
    return create_contact_date_array(all_messages)


def main():
    bring_all_mess()


if __name__ == '__main__':
    main()


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