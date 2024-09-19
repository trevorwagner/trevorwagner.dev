from datetime import datetime

from src.generators.dates.timestamps import timestamp_blog_post_format

test_time = datetime.fromisoformat("2023-07-08T15:31:00-05:00")


def test_formats_timestamp_as_expected():
    result = timestamp_blog_post_format(test_time)

    assert result == 'Jul 8, 2023'
