from airium import Airium


def hamburger_button(a: Airium):
    with a.div(id="hamburger"):
        a.span()
        a.span()
        a("&nbsp;")
    return
