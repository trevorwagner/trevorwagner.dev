from airium import Airium

from .navigation_menu import navigation_menu
from .social_media_links import social_media_links


def overlay_menu(a: Airium, entry):
    with a.div(id="overlay-menu"):
        navigation_menu(a, entry)
        social_media_links(a, reverse=False)

    return
