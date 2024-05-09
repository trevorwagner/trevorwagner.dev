from datetime import datetime
from xml.sax.saxutils import escape
from zoneinfo import ZoneInfo

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


def build_rss_for_blog_posts(posts):
    rss = "".join(
        [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
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

    for post in posts:
        new_item = "".join(
            [
                "\n\t<item>",
                f"\n\t\t<title>{post.page.title}</title>",
                f"\n\t\t<link>https://trevorwagner.dev{escape(post.page.relative_path)}</link>",
                f"\n\t\t<pubDate>{timestamp_rfc_822(post.published)}</pubDate>",
                # TODO: Add summaries to each blog post MD, to use for Description here.
                # TODO: Add summary element to manifest generation script.
                # '\n\t\t<description>{}</description>.format()'.format(escape(post["description"])),
                f"\n\t\t<guid>https://trevorwagner.dev{escape(post.page.relative_path)}</guid>"
                "\n\t</item>",
            ]
        )

        channel = "".join([channel, new_item])

    channel = "".join([channel, "\n\n</channel>"])

    rss = "".join([rss, channel])
    rss = "".join([rss, "\n\n</rss>"])

    return rss
