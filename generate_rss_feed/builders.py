from airium import Airium
from datetime import datetime
from markdown import markdown
from xml.sax.saxutils import escape
from zoneinfo import ZoneInfo

from generate_html.html_components import photo_credit


build_time = datetime.now()


def timestamp_rfc_822(time):
    timestamp = time.replace(tzinfo=ZoneInfo("America/Chicago"))
    return timestamp.strftime("%a, %d %b %Y %H:%M:%S %z")


metadata = {
    "title": "trevorwagner.dev - Blog",
    "description": "RSS Feed for new blog posts on trevorwagner.dev",
    "language": "en-us",
    "link": "https://www.trevorwagner.dev/blog/",
    "lastBuildDate": timestamp_rfc_822(build_time),
    "self": "https://www.trevorwagner.dev/blog/feed/",
    "copyright": f'{build_time.strftime("%Y")} Upstream Consulting LLC. All rights reserved.',
}


def build_content_html_for_post(post):
    a = Airium()

    with a.div():
        if post.cover_photo is not None:
            with a.div():
                a.img(src=post.cover_photo.url)

        a(markdown(post.page.md_file.page_content.replace('(/', '(https://www.trevorwagner.dev/')))

        if post.cover_photo is not None:
            photo_credit(a, post.cover_photo)
        with a.p():
            a.href(_t="More posts", href="https://trevorwagner.dev/blog/")
        a.hr()

        with a.p():
            a("&#169; " + metadata["copyright"])

    return str(a)


def build_rss_for_blog_posts(posts):
    rss = "".join(
        [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '\n<rss version="2.0"',
            '\n\txmlns:atom="http://www.w3.org/2005/Atom"',
            '\n\txmlns:dc="http://purl.org/dc/elements/1.1/"',
            '\n\txmlns:content="http://purl.org/rss/1.0/modules/content/"',
            " >",
        ]
    )

    channel = "".join(
        [
            "\n\n<channel>",
            f'\n\t<title>{escape(metadata["title"])}</title>',
            f'\n\t<link>{metadata["link"]}</link>',
            f'\n\t<description>{escape(metadata["description"])}</description>',
            f'\n\t<lastBuildDate>{metadata["lastBuildDate"]}</lastBuildDate>',
            f'\n\t<language>{metadata["language"]}</language>',
            f'\n\t<atom:link href="{escape(metadata["self"])}" rel="self" type="application/rss+xml" />',
            f'\n\t<copyright>{escape(metadata["copyright"])}</copyright>',
        ]
    )

    for post in posts[:20]:
        new_item = "".join(
            [
                "\n\t<item>",
                f"\n\t\t<title>{post.page.title}</title>",
                f"\n\t\t<link>https://trevorwagner.dev{escape(post.page.relative_path)}</link>",
                f"\n\t\t<pubDate>{timestamp_rfc_822(post.published)}</pubDate>",
                # TODO: Add summaries to each blog post MD, to use for Description here.
                # TODO: Add summary element to manifest generation script.
                # f'\n\t\t"<description><![CDATA[lorem ipsum]]></description>',
                f"\n\t\t<guid>https://trevorwagner.dev{escape(post.page.relative_path)}</guid>",
                f'\n\t\t<enclosure url="{post.cover_photo.url}" length="{post.cover_photo.get_attibute_value_for_key('file_content_length')}" type="{post.cover_photo.get_attibute_value_for_key('file_content_type')}"/>',
                f"\n\t\t<content:encoded><![CDATA[{build_content_html_for_post(post)}]]></content:encoded>",
                "\n\t</item>",
            ]
        )

        channel = "".join([channel, new_item])

    channel = "".join([channel, "\n\n</channel>"])

    rss = "".join([rss, channel])
    rss = "".join([rss, "\n\n</rss>"])

    return rss
