"""
Manage time log entries from https://toggl.com
"""
import re
import json
import logging
import datetime
from os.path import dirname, join

import yaml
import requests
from tzlocal import get_localzone


class Connect(object):
    def __init__(self, config=None):
        """Initialise

        *config* key to use, this is the key in the config file,
        defaults to *default*. Every key in the config is extended
        from default config settings.

        """
        with open(join(dirname(__file__), '../resource/toggl.yaml')) as config_file:
            config_data = yaml.load(config_file)

        if not config:
            self.config = config_data['default']
        else:
            if config_data.get(config):
                self.config = config_data['default'].update(config_data[config])
            else:
                raise KeyError('Failed to load config {0}'.format(config))

        self.url = self.config['url']
        self.api_key = self.config['api_key']
        self.time_period = self.config.get('time_period', 15)
        self.tag_as_read = self.config.get('tag', 'read')
        self.filter = self.config.get('filter', '.*')

    def _filter(self, data, ignore_marked):
        """Filter *data* dictionaries

        *data* dictionary containing time log entries
        *ignore_marked* check for marked tag and ignore time log

        """
        return_data = list()
        for each_data in data:
            is_valid = True
            if not re.match(self.filter, each_data.get('description', '')):
                is_valid = False
            if ignore_marked and self.tag_as_read in each_data.get('tags', list()):
                is_valid = False
            if is_valid:
                return_data.append(each_data)

        return return_data

    def get_time_logs(self, ignore_marked=True):
        """Get all time logs from toggl

        *ignore_marked* entries? if True check for the tags in every
        entry and filter them

        """
        start_date = datetime.datetime.now(
            tz=get_localzone()) - datetime.timedelta(self.time_period)

        end_date = datetime.datetime.now(tz=get_localzone())

        # Ignore microseconds
        start_date = start_date.replace(microsecond=0).isoformat()
        end_date = end_date.replace(microsecond=0).isoformat()

        payload = {
            'start_date': start_date,
            'end_date': end_date
            }

        try:
            request_object = requests.get(self.url,
                                          params=payload,
                                          auth=(self.api_key, 'api_token'))
        except Exception:
            logging.error('Failed to make request')
            raise

        if request_object.status_code != 200:
            logging.error('Failed to fetch time logs please see the response:\n{0}'
                          .format(request_object.content))
            return list()

        return self._filter(request_object.json(), ignore_marked)

    def update(self, data):
        """Update time log with *data*

        *data* toggl entry log to be updated

        """
        old_id = data.get('id')
        data.pop('id')
        url = '{0}/{1}'.format(self.url, old_id)
        request_object = requests.put(
            url,
            auth=(self.api_key, 'api_token'),
            data=json.dumps({'time_entry': data}))

        if request_object.status_code != 200:
            logging.error('Failed to update time log')

        return request_object

    def mark_as_read(self, data):
        """Mark toggl time log as read

        *data* dictionary containing a single log entry

        """
        if 'tags' in data.keys() and self.tag_as_read not in data['tags']:
            data['tags'].append(self.tag_as_read)
        else:
            data['tags'] = ['marked']
        return self.update(data)


if __name__ == '__main__':
    c = Connect()
    entr = c.get_time_logs()
    print entr
