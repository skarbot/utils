"""
Update time entries for Jira and redmine
"""
from __future__ import division
import logging

from jira import JIRA
from jira.exceptions import JIRAError

import toggl


def update_jira(url, username, password):
    """Update time logs in Jira

    Current implementation uses basic authentication,
    future version will have better auth. For simplicity
    the toggl log should have issue number as timelog
    description.

    *username* to use to connect to Jira
    *password* for Jira authentication

    """
    jira = JIRA(
        options={'server': url},
        basic_auth=(username, password))

    time_logs = toggl.Connect('jira')
    get_logs = time_logs.get_time_logs()

    for each_log in get_logs:
        issue_id = each_log.get('description')
        try:
            issue = jira.issue(issue_id)
        except JIRAError:
            logging.warning('Failed to find issue-id {0}'.format(issue_id))
            continue

        # Compute time in hours and round to two decimal places
        time_in_hours = round(each_log['duration']/(60*60), 2)
        jira.add_worklog(issue, time_in_hours, comment='Updated using Jira API')

