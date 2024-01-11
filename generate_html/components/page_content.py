from airium import Airium
import json
from markdown import markdown
from pathlib import Path
from xml.sax.saxutils import escape

from .blog_post_summary_link import blog_post_summary_link
from .blog_post_pub_date import blog_post_pub_date
from .cover_photo import cover_photo

DIST = Path(__file__).parent.resolve() / '../../_dist/'


# TODO: Figure this out when building the manifest/ returning page info via service.
def page_content(a: Airium, entry, content):
    with a.div(id="content"):
        if entry['page']['type'] == 'blogPost':
            a.h1(_t=escape(entry['page']['title']))
            a.time(_t=blog_post_pub_date(entry['page']['publishDate']))
            cover_photo(a, entry)

        else:
            if entry['slug'] != 'index':
                a.h1(_t=escape(entry['page']['title']))
            else:
                a.h1(_t="Welcome")

        if entry['slug'] != 'blog':
            # content = markdown(content)
            #
            # # TODO: Find a way to do this within the DOM (using something like lxml to work the tree as opposed to find- /
            # #  replacing text).
            # #
            # content = (content
            #            .replace('<h2>', '<h2 class="text-3xl leading-9 font-semibold pt-1 pb-2">')
            #            .replace('<h3>', '<h3 class="text-xl leading-9 font-semibold pt-1 pb-2">')
            #            .replace('<p>', '<p class="leading-7 mb-4">')
            #            .replace('<ul>', '<ul class="list-disc pl-5 leading-7 mb-4">')
            #            .replace('<li>', '<li class="pl-1 mt-2">')
            #            .replace('<pre>', '<pre class="mb-2">')
            #            )
            # a(content)
            a(markdown(content))
        else:
            # TODO(please): Instead of coupling functionality related to retrieving blog post entries to knowledge of where,
            #  the manifest is stored reading files, etc, create a service that can be query for metadata on pages like blog
            #  posts.
            #  -> Even better: find a way to decouple this component from any sort of querying at all.
            #
            manifest_file = DIST / 'site-manifest.json'
            with open(manifest_file) as f:
                manifest = json.loads(f.read())
                sorted_blog_posts = sorted(
                    [e for e in manifest['site'] if e['page']['type'] == 'blogPost'],
                    key=lambda i: i["page"]['publishDate'],
                    reverse=True
                )

                with a.div():
                    for post in sorted_blog_posts:
                        blog_post_summary_link(a, post)

    return
