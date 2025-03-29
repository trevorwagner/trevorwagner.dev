from airium import Airium
from markdown import markdown

from src.generators.html.opengraph import assemble_opengraph_data_for_page
from src.generators.html.components import (
    footer_content,
    header,
    overlay_menu,
    page_content,
    page_title,
    photo_credit,
)
from src.inventory import Page


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

            a('<link rel="preconnect" href="https://fonts.googleapis.com">')
            a('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
            a(
                '<link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap" rel="stylesheet">'
            )

            a(
                '<script async src="https://us.umami.is/script.js" data-website-id="72e1cfab-c988-430b-9f25-1f52cf8720f4"></script>'
            )

            a.link(rel="stylesheet", href="/css/styles.css", media="screen")

            if page.relative_path == "/blog/":
                a.link(rel="stylesheet", href="/css/layout/blog-home.css")

            if page.type == "blogPost":
                a.link(rel="stylesheet", href="/css/layout/blog-post.css")

                a.script(src="/js/lib/highlightjs/11.11.1/js/highlight.min.js")

                if 'class="language-gherkin"' in page.prepared_content:
                    a.script(src="/js/lib/highlightjs/11.11.1/js/gherkin.min.js")

                a.link(
                    rel="stylesheet",
                    href="/js/lib/highlightjs/11.11.1/css/default-dark.css",
                )

            a.link(
                rel="canonical",
                href=f"https://www.trevorwagner.dev{page.relative_path}",
            )

            if page.relative_path == "/experience/":
                a.link(rel="stylesheet", href="/css/resume.css")

            if page.relative_path == "/contact/":
                a.script(src="/js/contact-form.js")

        with a.body().div(klass="w-page"):
            header(a, page)
            overlay_menu(a, page)
            with a.main():
                page_content(a, page)
            with a.footer():
                footer_content(a)

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


def build_content_html_for_post(post, rss_metadata):
    a = Airium()

    with a.div():
        if post.cover_photo is not None:
            with a.div():
                with a.picture():
                    a.img(src=post.cover_photo.variants[0].url)

        a(
            markdown(
                post.page.prepared_content.replace(
                    "(/", "(https://www.trevorwagner.dev/"
                )
            )
        )

        if post.cover_photo is not None:
            photo_credit(a, post.cover_photo)
        with a.p():
            a.a(_t="More posts", href="https://www.trevorwagner.dev/blog/")
        with a.p():
            a.a(_t="Contact", href="https://www.trevorwagner.dev/contact/")
        a.hr()

        with a.p():
            a("&#169; " + rss_metadata.copyright)

    return str(a)
