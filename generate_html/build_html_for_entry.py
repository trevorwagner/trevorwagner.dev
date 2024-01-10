from airium import Airium

from .assemble_opengraph_data import assemble_opengraph_data_for_entry

from .components.footer import footer
from .components.header import header
from .components.overlay_menu import overlay_menu
from .components.page_content import page_content
from .components.page_title import page_title


def build_html_for_entry(entry, matter, content):
    a = Airium()

    a('<!DOCTYPE html>')

    with a.html(lang="en"):

        with a.head():
            a.meta(charset="utf-8")

            a.meta(name='author', content='Trevor Wagner')
            a.meta(name="viewport", content="width=device-width, initial-scale=1.0")
            for key, value in assemble_opengraph_data_for_entry(entry, matter, content).items():
                a.meta(property=key, content=value)

            page_title(a, entry)
            # a('<script async src="https://us.umami.is/script.js" data-website-id="72e1cfab-c988-430b-9f25-1f52cf8720f4"></script>')

            a.link(rel="stylesheet", href="/css/styles.css")

            if entry['page']['type'] == 'blogPost':
                a.script(src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js")
                a.link(rel="stylesheet",
                       href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/base16/default-dark.css")

            a.meta(name="viewport", content="width=device-width, initial-scale=1.0")

        with a.body():
            header(a, entry)
            overlay_menu(a, entry)
            with a.div():
                page_content(a, entry, content)
                footer(a)

            a.script(type="text/javascript", src="/js/slidedown-menu.js")
            a.script(_t="hljs.highlightAll();")

    return str(a)
