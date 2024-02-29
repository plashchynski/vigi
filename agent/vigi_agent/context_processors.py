import datetime
import humanize

def utility_processor():
    def format_time(time):
        # format time as HH:MM:SS
        return time.replace('-', ':')

    def format_duration(duration):
        if duration is None:
            return "N/A"
        # format duration as HH:MM:SS
        return humanize.naturaldelta(datetime.timedelta(seconds=duration))

    return dict(
            format_time=format_time,
            format_duration=format_duration
        )
