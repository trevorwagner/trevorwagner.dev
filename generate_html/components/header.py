from airium import Airium

from .hamburger_button import hamburger_button
from .navigation_menu import navigation_menu
from .social_media_links import social_media_links


def header(a: Airium, entry):
    with a.header():
        hamburger_button(a)

        with a.h1():
            a.a(_t="Trevor Wagner", href="/")
        a.p(_t="Project-Focused Software Engineer, QA Automation")

        navigation_menu(a, entry)
        social_media_links(a, reverse=False)

        a.div(klass="clear-both")
    return
