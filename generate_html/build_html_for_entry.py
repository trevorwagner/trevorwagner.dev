from airium import Airium

from assemble_opengraph_data import assemble_opengraph_data_for_entry

from components.page_content import page_content
from components.header import header
from components.footer import footer
from components.page_title import page_title


def build_html_for_entry(entry, matter, content):
    a = Airium()

    a('<!DOCTYPE html>')

    with a.html(lang="en"):

        with a.head():
            a.meta(charset="utf-8")

            for key, value in assemble_opengraph_data_for_entry(entry, matter, content).items():
                a.meta(property=key, content=value)

            page_title(a, entry)
            # a('<script async src="https://us.umami.is/script.js" data-website-id="72e1cfab-c988-430b-9f25-1f52cf8720f4"></script>')

            a.script(src="https://cdn.tailwindcss.com")

            if entry['page']['type'] == 'blogPost':
                a.script(src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js")
                a.link(rel="stylesheet",
                       href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/base16/default-dark.css")

        with a.body(klass="subpixel-antialiased"):
            header(a, entry)

            with a.div(klass="lg:ml-96 px-16 height-full max-w-6xl"):

                with a.div():
                    page_content(a, entry, content)

                    a.div(klass="clear-both")

                footer(a)
            a.script(_t="hljs.highlightAll();")

    return str(a)
