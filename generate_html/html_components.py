from airium import Airium
from datetime import datetime
from xml.sax.saxutils import escape
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from markdown import markdown

from inventory_service import Image, Page, BlogPost, engine
from generate_html.timestamps import timestamp_blog_post_format


def blog_post_summary_link(a: Airium, post: BlogPost):
    with a.div(klass="post-summary"):
        a.img(src=post.thumbnail.url, alt=escape(post.page.title))
        with a.a(href=post.page.relative_path):
            a.h2(_t=escape(post.page.title))
        a.time(datetime=post.published.replace(tzinfo=ZoneInfo("America/Chicago")).strftime('%Y-%m-%dT%H:%M:%S.000%z'), _t=escape(timestamp_blog_post_format(post.published)))
        a.div(klass="clear-both")
    return


def cover_photo(a: Airium, page: Page):
    with a.div(klass="cover-photo"):
        a.img(src=page.blog_post.cover_photo.url)
        photo_credit(a, page.blog_post.cover_photo)
    return


def footer(a: Airium):
    with a.footer():
        a.hr()
        a.p(
            _t=f"&#169; {datetime.now().strftime('%Y')} Upstream Consulting LLC. All Rights Reserved."
        )
    return


def hamburger_button(a: Airium):
    with a.div(id="hamburger"):
        a.span()
        a.span()
        a("&nbsp;")
    return


def header(a: Airium, page: Page):
    with a.header():
        hamburger_button(a)

        with a.h1():
            a.a(_t="Trevor Wagner", href="/")
        a.p(_t="Project-Focused Software Engineer, QA Automation")

        navigation_menu(a, page)
        social_media_links(a, reverse=False)

        a.div(klass="clear-both")
    return


menu_items = [
    {"name": "Experience", "path": "/experience/"},
    {"name": "Services", "path": "/services/"},
    {"name": "Blog", "path": "/blog/"},
    {"name": "Privacy Policy", "path": "/privacy-policy/"},
]


def navigation_menu(a: Airium, page: Page):
    with a.ul(klass="navigation"):
        for item in menu_items:
            if page.relative_path == item["path"]:
                a.li(_t=item["name"])
            else:
                with a.li():
                    a.a(_t=item["name"], href=item["path"])
    return


def overlay_menu(a: Airium, page: Page):
    with a.div(id="overlay-menu"):
        navigation_menu(a, page)
        social_media_links(a, reverse=False)
    return


def page_content(a: Airium, page: Page):
    with a.div(id="content"):
        a.h1(_t=escape(str(page.title)))
        if page.type == "blogPost":
            a.time(datetime=page.blog_post.published.replace(tzinfo=ZoneInfo("America/Chicago")).strftime('%Y-%m-%dT%H:%M:%S.000%z'), _t=timestamp_blog_post_format(page.blog_post.published))
            cover_photo(a, page)

        if page.relative_path != "/blog/":
            a(markdown(str(page.md_file.page_content)))
        else:
            with Session(engine) as session:
                blog_posts = (
                    session.query(BlogPost)
                    .join(Page)
                    .filter(Page.draft == False)
                    .order_by(BlogPost.published.desc())
                    .all()
                )
                for post in blog_posts:
                    blog_post_summary_link(a, post)
    return


def page_title(a: Airium, page: Page):
    if page.relative_path == "/":
        a.title(_t="Trevor Wagner | Project-Focused Software Engineer, QA Automation")
    else:
        if page.type == "blogPost":
            a.title(_t="Blog Post: {} | Trevor Wagner".format(escape(page.title)))
        else:
            a.title(_t="{} | Trevor Wagner".format(escape(page.title)))
    return


def photo_credit(a: Airium, image: Image):
    with a.p(_t="Photo by "):
        if image.attributes_contains_key("author_url"):
            a.a(
                _t=image.get_attibute_value_for_key("author_name"),
                href=f"{image.get_attibute_value_for_key('author_url')}?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash",
                target="blank",
            )

        else:
            a(image.get_attibute_value_for_key("author_name"))

        if image.attributes_contains_key("source_url"):
            a(" on ")
            a.a(
                _t="Unsplash",
                href=f"{image.get_attibute_value_for_key('source_url')}?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash",
                target="blank",
            )
    return


link_list = [
    {"name": "RSS Feed", "icon": "rss_icon.svg", "url": "/blog/feed/"},
    {
        "name": "GitHub",
        "icon": "github_logo.svg",
        "url": "https://github.com/trevorwagner",
    },
    {
        "name": "LinkedIn",
        "icon": "linkedin_logo.svg",
        "url": "https://www.linkedin.com/in/trevorwagner05/",
    },
]


def render_link(a: Airium, item):
    with a.li():
        with a.a(href=item["url"]):
            a.img(src="/images/{}".format(item["icon"]), alt=item["name"])
    return


def social_media_links(a: Airium, reverse=False):
    with a.ul(klass="social-media-links"):
        if reverse is False:
            for i in link_list:
                render_link(a, i)

        if reverse is True:
            for i in reversed(link_list):
                render_link(a, i)
    return
