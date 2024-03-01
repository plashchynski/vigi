# This file contains the context processors for views
# More info: https://flask.palletsprojects.com/en/3.0.x/templating/#context-processors

import datetime
import humanize

def utility_processor():
    def format_time(time):
        # format time as HH:MM:SS
        return time.replace('-', ':')

    def format_duration(duration):
        if duration is None:
            return "N/A"

        # format duration as n seconds, n minutes, n hours, n days, etc.
        return humanize.precisedelta(datetime.timedelta(seconds=duration))

    return dict(
            format_time=format_time,
            format_duration=format_duration
        )
