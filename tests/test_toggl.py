"""
Test toggl.py
"""
import json

import pytest

from utils import toggl


class RequestGet(object):
    def __init__(self):
        self.status_code = 200

    def json(self):
        return [{
            u'duronly': False,
            u'wid': 140891,
            u'description': u'XYZ_321',
            u'stop': u'2016-06-16T18:40:49+00:00',
            u'start': u'2016-06-16T18:09:00+00:00',
            u'at': u'2016-06-18T23:06:21+00:00',
            u'billable': False,
            u'duration': 1909,
            u'guid': u'2835f522-f475-44db-8071-1d067a3e6c88',
            u'id': 400163419,
            u'uid': 193045,
            u'tags': ['read']},
            {
            u'duronly': False,
            u'wid': 140891,
            u'description': u'XYZ_1',
            u'stop': u'2016-06-18T18:41:55+00:00',
            u'start': u'2016-06-18T18:21:00+00:00',
            u'at': u'2016-06-18T18:41:55+00:00',
            u'billable': False,
            u'duration': 1256,
            u'guid': u'7ce55a02-92fd-4bbc-bbd2-feff6ba4a6b4',
            u'id': 400163568,
            u'uid': 193045},
            {
            u'duronly': False,
            u'wid': 140891,
            u'uid': 193045,
            u'stop': u'2016-06-18T19:15:49+00:00',
            u'start': u'2016-06-18T18:47:24+00:00',
            u'at': u'2016-06-18T19:15:49+00:00',
            u'billable': False,
            u'duration': 1706,
            u'tags': ['read'],
            u'guid': u'77f22e82-ad1b-4d9f-b489-ed3bd56d2df5',
            u'id': 400164008}]


class RequestPut(object):
    def __init__(self, data):
        self.data = data
        self.status_code = 200

    def json(self):
        """Decode json data"""
        return json.loads(self.data)['time_entry']


def test_initialisation_with_incorrect_key():
    with pytest.raises(KeyError) as error:
        toggl.Connect('invalid_key')


def test_get_time_logs(monkeypatch):
    """Test time log query"""
    monkeypatch.setattr('requests.get', lambda x, params, auth: RequestGet())

    connect = toggl.Connect()
    # Test if marked fields are ignored
    assert len(connect.get_time_logs(ignore_marked=True)) == 1

    # Test for filtered description with ignore_marked false
    connect.filter = '\w{3}_\d*'
    assert len(connect.get_time_logs(ignore_marked=False)) == 2

    # Test for filtered data with ignore_marked True
    assert connect.get_time_logs(ignore_marked=True)[0]['id'] == 400163568


def test_update(monkeypatch):
    """Test update functionality while marking entries"""
    monkeypatch.setattr('requests.put',
                        lambda url, auth, data: RequestPut(data))

    connect = toggl.Connect()
    connect.tag_as_read = 'test_tag'
    data = {
        u'duronly': False,
        u'wid': 140891,
        u'description': u'test project',
        u'stop': u'2016-06-16T18:40:49+00:00',
        u'start': u'2016-06-16T18:09:00+00:00',
        u'at': u'2016-06-19T04:36:33+00:00',
        u'billable': False,
        u'tags': ['my_tag'],
        u'duration': 1909,
        u'guid': u'2835f522-f475-44db-8071-1d067a3e6c88',
        u'id': 400163419,
        u'uid': 193045}
    assert connect.mark_as_read(data).json()['tags'] == ['my_tag', 'test_tag']
