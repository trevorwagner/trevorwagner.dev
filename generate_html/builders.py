from airium import Airium

from generate_html.opengraph import assemble_opengraph_data_for_page
from generate_html.html_components import (
    footer,
    header,
    overlay_menu,
    page_content,
    page_title,
)
from inventory_service import Page


def build_html_for_page(page: Page):
    a = Airium()

    a("<!DOCTYPE html>")
    with a.html(lang="en"):

        with a.head():
            a.meta(charset="utf-8")

            a.meta(name="author", content="Trevor Wagner")
            a.meta(name="viewport", content="width=device-width, initial-scale=1.0")

            if page.relative_path != "/blog/":
                for key, value in assemble_opengraph_data_for_page(page).items():
                    a.meta(property=key, content=value)

            page_title(a, page)
            a.link(
                rel="canonical",
                href=f"https://www.trevorwagner.dev{page.relative_path}",
            )
            a(
                '<script async src="https://us.umami.is/script.js" data-website-id="72e1cfab-c988-430b-9f25-1f52cf8720f4"></script>'
            )

            a.link(rel="stylesheet", href="/css/styles.css")

            if page.type == "blogPost":
                a.script(src="/js/lib/highlightjs/11.9.0/js/highlight.min.js")
                if 'class="language-gherkin"' in page.md_file.page_content:
                    a.script(src="/js/lib/highlightjs/11.9.0/js/gherkin.min.js")
                a.link(
                    rel="stylesheet",
                    href="/js/lib/highlightjs/11.9.0/css/default-dark.css",
                )
            if page.relative_path == "/contact/":
                a.script(src="/js/contact-form.js")

        with a.body():
            header(a, page)
            overlay_menu(a, page)
            with a.div():
                page_content(a, page)
                footer(a)

            a.script(src="/js/slidedown-menu.js")
            if page.type == "blogPost":
                a.script(_t="hljs.highlightAll();")

            if page.relative_path == "/contact/":
                a.script(
                    _t="\t"
                    + "window.onload = function() {\n\t\t"
                    + "const formElement = buildContactForm();\n\t\t"
                    + "document.getElementById('contact-form').innerHTML = formElement.outerHTML;\n\t"
                    + "}"
                )

    return str(a)
