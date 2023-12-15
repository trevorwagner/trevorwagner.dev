from airium import Airium

from .navigation_menu import navigation_menu


def header(a: Airium, entry):
    with a.header(
            klass="relative lg:fixed lg:bottom-0 lg:left-0 lg:top-0 bg-black w-full lg:w-96 py-10 px-16 lg:p-10 lg:pt-24"):
        with a.div(klass="lg:mb-16"):
            with a.h1():
                a.a(_t="Trevor Wagner", href="/", klass="text-white text-lg")
            a.p(_t="Project-Focused Software Engineer, QA Automation", klass="text-zinc-400")

        navigation_menu(a, entry)
    return
