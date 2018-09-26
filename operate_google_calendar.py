#!/usr/bin/env python

import os, sys
import datetime
from pprint import pprint

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import string

SYS_TIMEZONE = 'Asia/Hong_Kong'

CALENDAR_SCOPES = 'https://www.googleapis.com/auth/calendar'
CWD = os.path.dirname(os.path.abspath(__file__))
TOKEN_JSON_PATH = os.path.join(CWD,'token.json')

CREDENTIAL_JSON_PATH = os.path.join(CWD,'credential.json')

# If modifying these scopes, delete the file token.json.
# https://developers.google.com/identity/protocols/googlescopes

class google_calendar_event():
    @property
    def name(self): return self._name

    @property
    def description(self): return self._description

    @property
    def start(self): return self._start

    @property
    def end(self): return self._end

    def __init__(self, name, description, start, end):
        # self.eventbite_event_json = json_in
        self._name = name
        self._description = description
        self._start = start
        self._end = end

    # TODO: need a better name
    def get_event_dict(self  ):
        # return the basic set for creat event
        try:
            basic_set_to_google_cal={
                'summary': self._name,
                'description': self._description ,
                'start': {'date':self._start,'timeZone': SYS_TIMEZONE,},
                'end': {'date':self._end,'timeZone': SYS_TIMEZONE,},
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                    ],
                },
            }
            return basic_set_to_google_cal
        except Exception as e:
            raise e


class google_login_helper():
    def __init__(self, token_json_path, credential_json_path, required_scopes):
        try:
            store = file.Storage(token_json_path)
            creds = store.get()
            if not creds or creds.invalid:
                flow = client.flow_from_clientsecrets(credential_json_path, required_scopes)
                creds = tools.run_flow(flow, store)
            service = build('calendar', 'v3', http=creds.authorize(Http()))
            self.active_service = service

        except Exception as e:
            raise e


class google_calendar_helper(google_login_helper):
    def __init__(self, token_json_path, credential_json_path, required_scopes):
        super().__init__(token_json_path, credential_json_path, required_scopes)

    def get_user_calendar_list(self):
        user_calendar_list = {}
        page_token = None
        try:
            while True:
                recv_calendar_list = self.active_service.calendarList().list(pageToken=page_token).execute()
                for calendar_list_entry in recv_calendar_list['items']:
                    cal_id = calendar_list_entry['id']
                    cal_name = calendar_list_entry['summary']
                    user_calendar_list[cal_name]=cal_id

                page_token = recv_calendar_list.get('nextPageToken')
                if not page_token:
                    break
            return user_calendar_list

        except Exception as e:
            raise e

    def get_calendar_list_id(self, calendar_list_name):
        try:
            _user_calendar_list = self.get_user_calendar_list()
            if calendar_list_name in  _user_calendar_list:
                return _user_calendar_list[calendar_list_name]

        except Exception as e:
            raise e

    def insert_event_into_calendar(self,calendar_list_name, event_to_insert):
        try:
            cal_id = self.get_calendar_list_id(calendar_list_name)
            event = self.active_service.events().insert(calendarId=cal_id, body=event_to_insert).execute()

            return self

        except Exception as e:
            print('haha')
            pprint(event_to_insert)
            raise e

def main():
    # google service oauth prepar
    google_cal_service = google_calendar_helper(TOKEN_JSON_PATH,CREDENTIAL_JSON_PATH,CALENDAR_SCOPES)
    # google_calendar_service = login_oauth(TOKEN_JSON_PATH,CREDENTIAL_JSON_PATH,CALENDAR_SCOPES)

    # pprint(get_user_calendar_list(service))

    # # # # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    # events_result = service.events().list(calendarId='test_calendar_list', timeMin=now,
    #                                     maxResults=10, singleEvents=True,
    #                                     orderBy='startTime').execute()
    # events = events_result.get('items', [])

    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])




if __name__ == '__main__':
    main()
