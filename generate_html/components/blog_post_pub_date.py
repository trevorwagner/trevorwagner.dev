from zoneinfo import ZoneInfo
from datetime import datetime

from re import sub


def blog_post_pub_date(timestamp):
    date = datetime.fromtimestamp(timestamp, tz=ZoneInfo("America/Chicago"))
    day_non_padded = sub(r'^0', '', date.strftime('%d'))
    return date.strftime('%b {}, %Y').format(day_non_padded)
