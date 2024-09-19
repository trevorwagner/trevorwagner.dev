from datetime import datetime

from src.generators.dates.timestamps import timestamp_opengraph_format

test_time = datetime.fromisoformat("2023-07-08T15:31:00-05:00")

def test_formats_timestamp_as_expected():
    result = timestamp_opengraph_format(test_time)

    assert result == "2023-07-08T15:31:00-05:00"
