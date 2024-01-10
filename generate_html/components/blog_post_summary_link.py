from airium import Airium

from xml.sax.saxutils import escape
from .blog_post_pub_date import blog_post_pub_date


def blog_post_summary_link(a: Airium, entry):
    with a.div(klass="post-summary"):
        with a.a(href=entry['page']['relativePath']):
            a.img(src=entry['coverPhoto']['thumbnail'])
            a.h2(_t=escape(entry['page']['title']))
            a.p(_t=escape(blog_post_pub_date(entry['page']['publishDate'])))
            a.div(klass="clear-both")
    return
