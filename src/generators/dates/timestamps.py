import re
from zoneinfo import ZoneInfo


def timestamp_blog_post_format(timestamp):
    """
    Formats timestamp as date string in the format (Jun 29, 2023)
    used within blog posts/ blog post summaries.
    """
    day_non_padded = re.sub(r"^0", "", timestamp.strftime("%d"))
    return timestamp.strftime("%b {}, %Y").format(day_non_padded)


def timestamp_opengraph_format(time):
    """
    Formats timestamp as date string in the format (ISO-8601)
    generally used for og:publish_date.
    """
    timestamp = time.replace(tzinfo=ZoneInfo("America/Chicago"))
    return timestamp.strftime("%Y-%m-%dT%H:%M:%S%:z")


def timestamp_rfc_822(time):
    timestamp = time.replace(tzinfo=ZoneInfo("America/Chicago"))
    return timestamp.strftime("%a, %d %b %Y %H:%M:%S %z")
