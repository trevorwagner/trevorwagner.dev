from airium import Airium

link_list = [
    {"name": "RSS Feed", "icon": "rss_icon.svg", "url": "/blog/feed/"},
    {"name": "GitHub", "icon": "github_logo.svg", "url": "https://github.com/trevorwagner"},
    {"name": "LinkedIn", "icon": "linkedin_logo.svg", "url": "https://www.linkedin.com/in/trevorwagner05/"},
]


def render_link(a: Airium, item):
    with a.li():
        with a.a(href=item["url"]):
            a.img(src="/images/{}".format(item["icon"]), alt=item['name'])
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
