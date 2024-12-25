from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1PWD7jUcMNfEpgCcpx1QGsficBqR3hG6QZiaOaCPbsfA'
SAMPLE_RANGE_NAME = 'industries!A2:B'


indexData = []

interestIndustries = []

columnCount = 0

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token-sheet.json'):
        creds = Credentials.from_authorized_user_file('token-sheet.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials-sheet.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token-sheet.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        indexData.clear()
        interestIndustries.clear()

        if not values:
            print('No data found.')
            
        # print('Property Address, City:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            if len(row) >= 1:
                indexData.append('%s' % (row[0]))
            if len(row) >= 2:
                interestIndustries.append('%s' % (row[0]))

        # print(getInterestIndustries())
    except HttpError as err:
        print(err)


def getColumnCount():
    columnCount = len(indexData)
    return columnCount

def getInterestIndustries():
    return interestIndustries

def insert_data(data_range, industry_value):
                
    data = [
        [industry_value]
    ]
    data_body = {
        'values': data
    }
    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token-sheet.json'):
        creds = Credentials.from_authorized_user_file('token-sheet.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials-sheet.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token-sheet.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Finally, call the API to write the data to the spreadsheet
        result1 = service.spreadsheets().values().update(
                spreadsheetId=SAMPLE_SPREADSHEET_ID,
                range=data_range,
                valueInputOption='USER_ENTERED',
                body=data_body
            ).execute()

        print('{0} data updated.'.format(result1.get('updatedCells')))
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()