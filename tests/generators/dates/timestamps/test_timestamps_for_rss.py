from datetime import datetime

from src.generators.dates.timestamps import timestamp_rfc_822

test_time = datetime.fromisoformat("2023-07-08T15:31:00-05:00")

def test_formats_timestamp_as_expected():
    result = timestamp_rfc_822(test_time)

    assert result == "Sat, 08 Jul 2023 15:31:00 -0500"