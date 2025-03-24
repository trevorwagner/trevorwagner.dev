from airium import Airium
from datetime import datetime
from xml.sax.saxutils import escape

from markdown import markdown

from src.inventory import Image, Page, BlogPost, engine, posts
from src.generators.dates.timestamps import (
    timestamp_blog_post_format,
    timestamp_opengraph_format,
)
from _static import php_contact_form_handler


def blog_post_summary_link(a: Airium, post: BlogPost):
    with a.div(klass="post-summary"):
        with a.a(href=post.page.relative_path):
            use_variants = list(
                filter(lambda v: int(v.width) <= 800, post.cover_photo.variants)
            )

            with a.picture():
                for variant in use_variants:
                    a.source(
                        type=variant.mime_type,
                        srcset=variant.url,
                    )
                a.img(src=use_variants[0].url, alt=escape(post.page.title))

        with a.a(href=post.page.relative_path):
            a.h2(_t=escape(post.page.title))
        a.time(
            _t=escape(timestamp_blog_post_format(post.published)),
            datetime=timestamp_opengraph_format(post.published),
        )
        a.div(klass="clear-both")
    return


def card_next_post(a: Airium, with_page: Page):
    with a.div(klass="c-next-blog-post"):
        a.h2(_t="Next Post")
        with a.ul():
            a.li().a(
                href=with_page.relative_path,
                _t=with_page.title,
            )
    return


def card_previous_post(a: Airium, with_page: Page):
    with a.div(klass="c-previous-blog-post"):
        a.h2(_t="Previous Post")
        with a.ul():
            a.li().a(
                href=with_page.relative_path,
                _t=with_page.title,
            )
    return


def card_recent_blog_posts_for_page(
    a: Airium, current_page: Page, limit: int, exclude_posts: list[BlogPost]
):
    with a.div(klass="c-recent-blog-posts"):
        section_heading = (
            "Recent Blog Posts"
            if current_page.type != "blogPost"
            else "More Recent Posts"
        )

        page_mask = None
        if current_page.type == "blogPost":
            page_mask = exclude_posts

        a.h2(_t=section_heading)

        recent_posts = posts.list_recent_posts(limit, page_mask)

        if len(recent_posts) > 0:
            with a.ul():
                for blog_post in recent_posts:
                    a.li().a(
                        href=blog_post.page.relative_path,
                        _t=blog_post.page.title,
                    )

        with a.p():
            a.a(href="/blog/", _t="More...")

    return


def contact_form(a: Airium, page: Page):
    with a.form(
        name="contact-form",
        id="contact-form",
        method="post",
        action=f"<?php echo htmlspecialchars('{page.relative_path}'); ?>",
        onsubmit="return handleFormSubmission()",
    ):
        a.noscript(
            _t="This form requires JavaScript. To continue, please enable JavaScript in your browser."
        )
    return


def cover_photo(a: Airium, page: Page):
    with a.div(klass="cover-photo"):
        with a.picture():
            use_variants = list(
                filter(
                    lambda v: 950 >= int(v.width) >= 500,
                    page.blog_post.cover_photo.variants,
                )
            )

            for variant in use_variants:
                a.source(
                    type=variant.mime_type,
                    srcset=variant.url,
                )
            a.img(
                src=use_variants[0].url,
                alt=page.blog_post.cover_photo.get_attibute_value_for_key(
                    "description"
                ),
            )
        photo_credit(a, page.blog_post.cover_photo)
    return


def footer_content(a: Airium, hidden=False):
    with a.div(klass="s-match-footer" if hidden is True else ""):
        a.p(
            _t=f"&#169; {datetime.now().strftime('%Y')} Upstream Consulting LLC. All Rights Reserved.",
            klass="detail",
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
        with a.div(klass="w-header"):
            hamburger_button(a)

            a.div(klass="headshot")

            with a.div(klass="w-nameplate"):
                with a.h1():
                    a.a(_t="Trevor Wagner", href="/")
                a.p(
                    _t="Project-Focused Software Engineer, QA Automation",
                    klass="detail",
                )

            navigation_menu(a, page)
            social_media_links(a, reverse=False)

            a.div(klass="clear-both")
    return


menu_items = [
    {"name": "Experience", "path": "/experience/"},
    {"name": "Services", "path": "/services/"},
    {"name": "Blog", "path": "/blog/"},
    {"name": "Privacy Policy", "path": "/privacy-policy/"},
    {"name": "Contact", "path": "/contact/"},
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
        with a.div(id="notices"):
            if page.relative_path == "/contact/":
                a(f"\n{php_contact_form_handler}\n")

        with a.div(klass="w-content-header"):
            with a.div(klass="w-page-title"):
                use_title = (
                    str(page.alt_title)
                    if page.alt_title is not None
                    else str(page.title)
                )
                a.h1(_t=escape(use_title))

            if page.type == "blogPost":
                with a.div(klass="w-publication-date"):
                    a.time(
                        _t=timestamp_blog_post_format(page.blog_post.published),
                        datetime=timestamp_opengraph_format(page.blog_post.published),
                        klass="detail",
                    )

        if page.type == "blogPost":
            cover_photo(a, page)

        if page.relative_path != "/blog/":
            a(markdown(str(page.prepared_content)))

            if page.relative_path == "/contact/":
                contact_form(a, page)

        else:
            blog_posts = posts.list_recent_posts(None, None)
            for post in blog_posts:
                blog_post_summary_link(a, post)

    if page.relative_path not in ["/privacy-policy/", "/blog/", "/404/", "/contact/"]:
        with a.div(klass="w-more-info"):

            if page.type == "blogPost":
                linked_blog_posts = [page.blog_post]

                next_post = posts.get_next_post(page.blog_post)
                previous_post = posts.get_previous_post(page.blog_post)

                if next_post is not None:
                    card_next_post(a, next_post.page)
                    linked_blog_posts.append(next_post)

                if previous_post is not None:
                    card_previous_post(a, previous_post.page)
                    linked_blog_posts.append(previous_post)

                card_recent_blog_posts_for_page(
                    a=a,
                    current_page=page,
                    limit=(5 - (len(linked_blog_posts) - 1)),
                    exclude_posts=linked_blog_posts,
                )

            else:
                card_recent_blog_posts_for_page(
                    a=a, current_page=page, limit=5, exclude_posts=[]
                )
    return


def page_title(a: Airium, page: Page):
    if page.type == "blogPost":
        a.title(_t="Blog Post: {} | Trevor Wagner".format(escape(page.title)))
    else:
        a.title(_t="{} | Trevor Wagner".format(escape(page.title)))
    return


def photo_credit(a: Airium, image: Image):
    with a.p(_t="Photo by ", klass="detail"):
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
    {"name": "RSS Feed", "icon": "rss_icon.svg", "url": "/blog/feed/", "klass": "rss"},
    {
        "name": "Contact",
        "icon": "email_icon.svg",
        "url": "/contact/",
        "klass": "contact",
    },
    {
        "name": "GitHub",
        "icon": "github_logo.svg",
        "url": "https://github.com/trevorwagner",
        "klass": "github",
    },
    {
        "name": "LinkedIn",
        "icon": "linkedin_logo.svg",
        "url": "https://www.linkedin.com/in/trevorwagner05/",
        "klass": "github",
    },
]


def render_link(a: Airium, item):
    with a.li():
        with a.a(href=item["url"], klass=item["klass"]):
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
