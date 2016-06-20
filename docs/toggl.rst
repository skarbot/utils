Toggl connector
================


Overview
---------

This very simple config based wrapper to query
toggl.com time entries. Once the entries are retrieved they
can be used to update any ticketing system like Jira,
redmine.

Configure
----------

The toggl wrapper depends on a YAML config which is placed
in the package resource directory. If you are using multiple
ticketing system you can have separate configuration for each one
of them. For example:

    .. code-block:: python

        default:
            url: to the toggl api page
            api_key: api key for user authentication
            time_period: duration for which records should be fetched, defaults to 15
            tag: to avoid entries being read twice once the entry is logged it should be tagged
            filter: takes regular expressions, this will be matched against description and only match values will be returned

If you have multiple tracking system you can create more keys in the config and pass the key.

Usage
------

Once configuration is complete, you can query time logs by

    .. code-block:: python

        connect = toggl.Connect()
        connect.get_time_logs()

To mark the record as read

    .. code-block:: python

        connect.mark_as_read(time_entry_data)
