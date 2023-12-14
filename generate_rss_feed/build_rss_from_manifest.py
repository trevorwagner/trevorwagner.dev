from datetime import datetime

build_time = datetime.now()

metadata = {
    "title": 'trevorwagner.dev - Blog',
    "description": 'RSS Feed for new blog posts on trevorwagner.dev',
    "language": 'en-us',
    "link": 'https://trevorwagner.dev/blog/',
    "lastBuildDate": build_time.strftime("%a, %d %b %Y"),
    "copyright": '{}  Upstream Consulting LLC. All rights reserved.'.format(build_time.strftime("%y"))
}


def build_rss_from_inventory(inventory):
    rss = ''.join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        '\n<rss version="2.0">'
    ])

    channel = ''.join([
        '\n<channel>',
        '\n\t<title>{}</title>'.format(metadata["title"]),
        '\n\t<link>{}</link>'.format(metadata["link"]),
        '\n\t<description>{}</description>'.format(metadata["description"]),
        '\n\t<lastBuildDate>{}</lastBuildDate>'.format(metadata["lastBuildDate"]),
        '\n\t<language>{}</language>'.format(metadata["language"]),
        '\n\t<copyright>{}</copyright>'.format(metadata["copyright"]),
    ])

    blog_posts = [e for e in inventory.site if e['type'] == 'blogPost']
    for post in blog_posts:

        new_item = ''.join([
            '\t<item>',
            '\n\t\t<title>{}</title>'.format(post["title"]),
            '\n\t\t<link>https://trevorwagner.dev/blog{}</link>'.format(post["relativePath"]),
            '\n\t\t<pubDate>{}</pubDate>'.format(datetime.fromtimestamp(
                post['publicationDate']).strftime("%a, %d %b %Y")
            ),
            # TODO: Add summaries to each blog post MD, to use for Description here.
            # TODO: Add summary element to manifest generation script.
            # '\n\t\t<description>{}</description>.format()'.format(post["description"]),
            '\n\t</item>'
        ])

        channel.join(new_item)

    channel.join('</channel>')

    rss.join(channel)
    rss.join('\n</rss>')

    return rss
