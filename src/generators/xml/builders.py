from collections import namedtuple
from xml.sax.saxutils import escape

from src.generators.html import build_content_html_for_post
from src.generators.dates import timestamp_rfc_822

SiteMetadata = namedtuple(
    "SiteMetadata", ["title", "language", "link", "description", "last_build_date", "self", "copyright"]
)


def build_rss_for_blog_posts(posts, metadata):
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
            f'\n\t<title>{escape(metadata.title)}</title>',
            f'\n\t<link>{metadata.link}</link>',
            f'\n\t<description>{escape(metadata.description)}</description>',
            f'\n\t<lastBuildDate>{metadata.last_build_date}</lastBuildDate>',
            f'\n\t<language>{metadata.language}</language>',
            f'\n\t<atom:link href="{escape(metadata.self)}" rel="self" type="application/rss+xml" />',
            f'\n\t<copyright>{escape(metadata.copyright)}</copyright>',
        ]
    )

    for post in posts[:20] :
        if post.page.draft == False:
            new_item = "".join(
                [
                    "\n\t<item>",
                    f"\n\t\t<title>{post.page.title}</title>",
                    f"\n\t\t<link>https://www.trevorwagner.dev{escape(post.page.relative_path)}</link>",
                    f"\n\t\t<pubDate>{timestamp_rfc_822(post.published)}</pubDate>",
                    # TODO: Add summaries to each blog post MD, to use for Description here.
                    # TODO: Add summary element to manifest generation script.
                    # f'\n\t\t"<description><![CDATA[lorem ipsum]]></description>',
                    f"\n\t\t<guid>https://www.trevorwagner.dev{escape(post.page.relative_path)}</guid>",
                    f'\n\t\t<enclosure url="{post.cover_photo.variants[0].url}" length="{post.cover_photo.variants[0].length}" type="{post.cover_photo.variants[0].mime_type}"/>',
                    f"\n\t\t<content:encoded><![CDATA[{build_content_html_for_post(post, metadata)}]]></content:encoded>",
                    "\n\t</item>",
                ]
            )

            channel = "".join([channel, new_item])

    channel = "".join([channel, "\n\n</channel>"])

    rss = "".join([rss, channel])
    rss = "".join([rss, "\n\n</rss>"])

    return rss


def build_sitemap_for_pages(pages):

    sitemap = "".join(
        [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        ]
    )

    for page in pages:
        if page.draft == False:
            timestamp = page.md_file.mod_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            new_item = "".join(
                [
                    "\n\t<url>",
                    f"\n\t\t<loc>https://www.trevorwagner.dev{page.relative_path}</loc>",
                    f"\n\t\t<lastmod>{timestamp}</lastmod>",
                    "\n\t</url>",
                ]
            )
            sitemap = "".join([sitemap, new_item])

    sitemap = "".join([sitemap, "\n</urlset>"])

    return sitemap

