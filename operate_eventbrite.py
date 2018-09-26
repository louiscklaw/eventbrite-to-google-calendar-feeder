#!/usr/bin/env python

import os,sys
import requests
import json
from pprint import pprint
from collections import OrderedDict

from operate_google_calendar import google_calendar_event


EVENT_BRITE_API_VER='v3'
EVENT_BRITE_API_HOST='/'.join([os.getenv('EVENT_BRITE_API_HOST'), EVENT_BRITE_API_VER])

EVENT_BRITE_TEST_TOKEN=os.getenv('EVENT_BRITE_TOKEN')

class eventbite_event():
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

    def parse_event_bite_event(self, json_in):
        return self

    def get_google_cal_event_json(self):
        try:
            out = google_calendar_event(
                self._name['text'],
                self._description['text'],
                self._start['local'].split('T')[0],
                self._end['local'].split('T')[0]
            ).get_event_dict()

            return out
        except Exception as e:

            raise e

class requests_helper():
    def __init__(self, api_host, token):
        self.api_host = api_host
        self.token = token

    def get_call_path(self, end_point):
        try:
            call_path = '/'.join([self.api_host,end_point])
            if len(end_point) == 0:
                call_path = self.api_host
            return call_path
        except Exception as e:
            pprint(end_point)
            raise e


    def make_get_call(self, end_point, d_payload):
        od_search_param = OrderedDict()
        try:
            call_path = self.get_call_path(end_point)

            # d_payload['token'] = self.token
            od_search_param['token']=self.token
            for k,v in d_payload.items():
                od_search_param[k]=v


            r = requests.get( call_path,params=od_search_param)

            if (404 == r.status_code):
                raise HTTPS_ERROR_404


            return r
        except Exception as e:
            print('error during make_get_call')
            pprint(r.url)
            pprint(end_point)
            raise e

class event_brite_api_helper(requests_helper):
    def __init__(self, token):
        super().__init__(EVENT_BRITE_API_HOST, token)

    def get_user(self):
        # users/me/: Shows information about the current user
        return self.make_get_call('users/me',{})

    def get_events(self, d_payload):
        # GET /events/search/¶
        # Allows you to retrieve a paginated response of public event objects from across Eventbrite’s directory, regardless of which user owns the event.

        return self.make_get_call('events/search', d_payload)

class event_brite_ETL_helper():

    def transform_json_to_event(self, json_in):
        l_event_out=[]
        try:
            l_events = json.loads(json_in)['events']
            for event in l_events:
                l_event_out.append(eventbite_event(
                    event['name'],
                    event['description'],
                    event['start'],
                    event['end']
                ))
            return l_event_out
        except Exception as e:
            raise e


class event_brite_helper(event_brite_api_helper, event_brite_ETL_helper):

    def extract_events_by_date(self, start_date, end_date):
        # encapsulated call only
        return self.get_events(
            {
                'start_date.range_start':start_date,
                'start_date.range_end':end_date
            }
        )

    def trans_events_by_date(self, start_date, end_date):
        try:
            json_events=self.extract_events_by_date(start_date, end_date)

            return self.transform_json_to_event(json_events.text)
        except Exception as e:
            raise e


    def load_events_by_date(self, start_date, end_date):
        try:
            d_events = self.trans_events_by_date(start_date, end_date)
            return d_events
        except Exception as e:
            raise e

    def extract_event_by_search(self, search_word):
        try:
            out = self.get_events(
                {
                    'q': search_word
                }
            )
            return out
        except Exception as e:
            pprint(out)
            raise e

    def trans_event_by_search(self, search_word):
        try:
            json_events=self.extract_event_by_search(search_word)

            return self.transform_json_to_event(json_events.text)
        except Exception as e:
            pprint(json_events)
            raise e

    def load_events_by_search(self, search_word):
        try:
            d_events = self.trans_event_by_search(search_word)

            return d_events
        except Exception as e:
            pprint(search_word)
            raise e
