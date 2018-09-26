#!/usr/bin/env python
# init_py_dont_write_bytecode

import os,sys
import requests
import unittest
from pprint import pprint
from unittest.mock import MagicMock, patch
import datetime
import json
from collections import OrderedDict


# target import
# from operate_eventbrite import *
import operate_eventbrite
from operate_google_calendar import *


# create shortcut less confusing
datetime2 = datetime.datetime
datetime2_now = datetime2.now
DATE_FMT_STRING = '%Y-%m-%d'
get_day = lambda x: (datetime.date.today()+datetime.timedelta(days=x)).strftime(DATE_FMT_STRING)

TODAY = get_day(0)+'T00:00:00'
TODAY_AND_1 = get_day(1)+'T00:00:00'
TODAY_AND_2 = get_day(2)+'T00:00:00'
TODAY_AND_7 = get_day(7)+'T00:00:00'
TEST_TIMEZONE = 'Asia/Hong_Kong'
TEST_CALENDAR = 'test_calendar_list'


# ENV SETTING
HTTPS_TEST_SERVER=os.getenv('HTTPBIN_SERVER')
STUB_GET_REQUESTS = '/'.join([HTTPS_TEST_SERVER,'get'])

# SETTING FOR GOOGLE CALENDAR
# settings file, credential file, token files
CALENDAR_SCOPES = 'https://www.googleapis.com/auth/calendar'
CWD = os.path.dirname(os.path.abspath(__file__))
TOKEN_JSON_PATH = os.path.join(CWD,'token.json')
CREDENTIAL_JSON_PATH = os.path.join(CWD,'credential.json')
TEST_CALENDAR = 'test_calendar_list'

# TEST SETTING
EVENT_BRITE_TEST_TOKEN=os.getenv('EVENT_BRITE_TEST_TOKEN')
EVENT_LOCATION='hong kong'
EVENT_BRITE_SEARCH_WORD='RICS Tai Kwun Symposium'


def setUpModule():
    print('setup (topic) module')
def tearDownModule():
    print('teardown (topic) module')

class TestEventBriteApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setup (topic) class')

    @classmethod
    def tearDownClass(cls):
        print('teardown (topic) class')

    def setUp(self):
        print('setup (topic) test')

    def tearDown(self):
        print('teardown (topic) test')

    def test_make_get_call(self, test_payload={'param1':'value1'}):
        # try to check the get parameters
        operate_eventbrite.EVENT_BRITE_API_HOST=STUB_GET_REQUESTS
        a = operate_eventbrite.requests_helper(STUB_GET_REQUESTS, EVENT_BRITE_TEST_TOKEN)
        req_call = a.make_get_call('', test_payload)

        httpbin_return=json.loads(req_call.text)
        self.assertIn('args',httpbin_return.keys())
        returned_arg = httpbin_return['args']

        self.assertEqual(200,int(req_call.status_code))
        for k,v in test_payload.items():
            self.assertIn(k,returned_arg.keys(), 'the wanted parameters not returning')
            self.assertIn(v, returned_arg[k],'the wanted values not returning')

    def test_make_get_call_search(self, search_word="Hong Kong"):
        self.test_make_get_call({'q':search_word})

    def test_extract_user_request(self):
        test_call=operate_eventbrite.event_brite_helper(EVENT_BRITE_TEST_TOKEN)
        user = test_call.get_user()


    def test_extract_events_by_date(self):
        # sample calling
        test_call=operate_eventbrite.event_brite_helper(EVENT_BRITE_TEST_TOKEN)
        call_result = test_call.extract_events_by_date( TODAY,TODAY_AND_1)


    def test_load_events_by_date(self, start_date=TODAY, end_date=TODAY_AND_1):
        EXPECTED_COMPONENTS = ['created', 'description']
        test_call=operate_eventbrite.event_brite_helper(EVENT_BRITE_TEST_TOKEN)
        call_result = test_call.load_events_by_date( start_date,end_date)

        check_event_0 = call_result[0]
        self.assertNotEqual('',check_event_0.name)

        return call_result

    def test_extract_event_by_search(self):
        test_call=operate_eventbrite.event_brite_helper(EVENT_BRITE_TEST_TOKEN)
        call_result = test_call.extract_event_by_search('Hong Kong')


    def test_load_events_by_search(self, search_word='Hong Kong'):
        test_call=operate_eventbrite.event_brite_helper(EVENT_BRITE_TEST_TOKEN)
        call_result = test_call.load_events_by_search(search_word)

        check_event_0 = call_result[0]
        self.assertNotEqual('',check_event_0.name)

        return call_result

    def test_insert_into_google_calendar_from_eventbrite(self, target_calendar_name=TEST_CALENDAR, event_brite_search_word=EVENT_BRITE_SEARCH_WORD):
        # for example , today as start date , tomorrow as stop day
        events_from_eventbrite = self.test_load_events_by_search(event_brite_search_word)

        google_service = google_calendar_helper(TOKEN_JSON_PATH, CREDENTIAL_JSON_PATH, CALENDAR_SCOPES)

        for event in events_from_eventbrite[0:1]:
            try:
                print('inserting events')
                google_service.insert_event_into_calendar(target_calendar_name, events_from_eventbrite[0].get_google_cal_event_json())

            except Exception as e:
                raise e

if __name__ == '__main__':
    unittest.main(verbosity=2)
