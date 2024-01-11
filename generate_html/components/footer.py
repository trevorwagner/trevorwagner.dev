from airium import Airium

from datetime import datetime


def footer(a: Airium):
    with a.footer():
        a.hr()
        a.p(_t="&#169; {} Upstream Consulting LLC. All Rights Reserved.".format(datetime.now().strftime('%Y')))

    return
