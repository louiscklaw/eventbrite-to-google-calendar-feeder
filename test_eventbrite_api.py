#!/usr/bin/env python
# init_py_dont_write_bytecode

import os,sys
import requests
import unittest
from pprint import pprint
from unittest.mock import MagicMock, patch
import datetime
import json

# target import
# from operate_eventbrite import *
import operate_eventbrite


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

# TEST SETTING
EVENT_BRITE_TEST_TOKEN=os.getenv('EVENT_BRITE_TEST_TOKEN')
EVENT_LOCATION='hong kong'



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

    def test_extract_user_request(self):
        test_call=operate_eventbrite.event_brite_ETL_helper(EVENT_BRITE_TEST_TOKEN)
        user = test_call.get_user()
        pprint(user.text)

    def test_extract_events_by_date(self):
        # sample calling
        test_call=operate_eventbrite.event_brite_ETL_helper(EVENT_BRITE_TEST_TOKEN)
        call_result = test_call.extract_events_by_date( TODAY,TODAY_AND_1)

    def test_load_events_by_date(self):
        EXPECTED_COMPONENTS = ['created', 'description']
        test_call=operate_eventbrite.event_brite_ETL_helper(EVENT_BRITE_TEST_TOKEN)
        call_result = test_call.load_events_by_date( TODAY,TODAY_AND_1)

        check_event_0 = call_result['events'][0]
        for component in EXPECTED_COMPONENTS:
            self.assertIn(component,check_event_0.keys(), ' the %s date not found' % component)





if __name__ == '__main__':
    unittest.main(verbosity=2)
