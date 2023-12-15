from airium import Airium

from datetime import datetime


def footer(a: Airium):
    with a.footer():
        a.p(
            _t="&#169; {} Upstream Consulting LLC. All Rights Reserved.".format(datetime.now().strftime('%Y')),
            klass="leading-7 pt-2 pb-2 text-zinc-400 border-t-[1px] border-zinc-400")

    return
