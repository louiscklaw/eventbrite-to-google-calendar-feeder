#!/usr/bin/env python

import os,sys
import requests
import json

from pprint import pprint

EVENT_BRITE_API_VER='v3'
EVENT_BRITE_API_HOST='/'.join([os.getenv('EVENT_BRITE_API_HOST'), EVENT_BRITE_API_VER])

EVENT_BRITE_TEST_TOKEN=os.getenv('EVENT_BRITE_TOKEN')

class requests_helper():
    def __init__(self, api_host, token):
        self.api_host = api_host
        self.token = token

    def get_call_path(self, end_point):
        try:
            pprint(end_point)

            call_path = '/'.join([self.api_host,end_point])
            if len(end_point) == 0:
                call_path = self.api_host
            return call_path
        except Exception as e:
            pprint(end_point)
            raise e


    def make_get_call(self, end_point, d_payload):
        try:
            call_path = self.get_call_path(end_point)

            d_payload['token'] = self.token
            r = requests.get( call_path,params=d_payload)

            if (404 == r.status_code):
                pprint(r.url)
            return r
        except Exception as e:
            pprint(r.url)
            pprint('haha')
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

class event_brite_ETL_helper(event_brite_api_helper):

    def transform_json_to_dict(self, json_in):
        dict_out={}
        try:
            dict_out = json.loads(json_in)
            return dict_out
        except Exception as e:
            raise e

    def extract_events_by_date(self, start_date, end_date):
        # encapsulated call only
        return self.get_events(
            {
                'start_date.range_start':start_date,
                'start_date.range_end':end_date
            }
        )

    def transform_events_by_date(self, start_date, end_date):
        try:
            json_events=self.extract_events_by_date(start_date, end_date)
            return self.transform_json_to_dict(json_events.text)
        except Exception as e:
            raise e

    def load_events_by_date(self, start_date, end_date):
        try:
            d_events = self.transform_events_by_date(start_date, end_date)
            return d_events
        except Exception as e:
            raise e
