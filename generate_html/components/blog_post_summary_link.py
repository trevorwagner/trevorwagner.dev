from airium import Airium

from xml.sax.saxutils import escape
from .blog_post_pub_date import blog_post_pub_date


def blog_post_summary_link(a: Airium, entry):
    with a.div(klass='my-2 pt-2 hover:bg-sky-50'):
        with a.a(href=entry['page']['relativePath'], klass="display-block py-2"):
            a.img(src=entry['coverPhoto']['thumbnail'], klass="float-right w-36 ml-8")
            a.h2(_t=escape(entry['page']['title']))
            a.p(_t=escape(blog_post_pub_date(entry['page']['publishDate'])), klass='leading-7 text-zinc-400')
            a.div(klass="clear-both")
    return
