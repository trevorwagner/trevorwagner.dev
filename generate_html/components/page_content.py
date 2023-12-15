from airium import Airium
import markdown
from xml.sax.saxutils import escape

from zoneinfo import ZoneInfo
from datetime import datetime

from re import sub

from .cover_photo import cover_photo


def get_blog_post_pub_date(timestamp):
    date = datetime.fromtimestamp(timestamp, tz=ZoneInfo("America/Chicago"))
    day_non_padded = sub(r'^0', '', date.strftime('%d'))
    return date.strftime('%b {}, %Y').format(day_non_padded)


def page_content(a: Airium, entry, content):
    if entry['page']['type'] == 'blogPost':
        a.h1(_t=escape(entry['page']['title']), klass="text-4xl subpixel-antialiased mt-16 font-semibold")
        a.p(_t=get_blog_post_pub_date(entry['page']['publishDate']), klass="text-zinc-500")
        cover_photo(a, entry)

    else:
        a.h1(_t=escape(entry['page']['title']),
             klass="text-4xl text-zinc-950 mt-20 font-semibold max-w-6xl mb-16")

    content = markdown.markdown(content)
    content = (content
               .replace('<h2>', '<h2 class="text-3xl leading-9 font-semibold pt-1 pb-2">')
               .replace('<h3>', '<h3 class="text-xl leading-9 font-semibold pt-1 pb-2">')
               .replace('<p>', '<p class="leading-7 mb-4">')
               .replace('<ul>', '<ul class="list-disc pl-5 leading-7 mb-4">')
               .replace('<li>', '<li class="pl-1 mt-2">')
               .replace('<pre>', '<pre class="mb-2">')
               )

    a(content)

    return
