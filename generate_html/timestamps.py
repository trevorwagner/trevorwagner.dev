import re


def timestamp_blog_post_format(timestamp):
    """
    Formats timestamp as date string in the format (Jun 29, 2023)
    used within blog posts/ blog post summaries.
    """
    day_non_padded = re.sub(r"^0", "", timestamp.strftime("%d"))
    return timestamp.strftime("%b {}, %Y").format(day_non_padded)


def timestamp_opengraph_format(timestamp):
    """
    Formats timestamp as date string in the format (???)
    generally used for og:publish_date.
    """
    return timestamp.strftime("").replace("%Y-%m-%dT%H:%M:%S%:z", "T")
