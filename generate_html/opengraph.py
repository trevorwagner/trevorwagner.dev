from xml.sax.saxutils import escape

from inventory_service import Page
from generate_html.timestamps import timestamp_opengraph_format


def assemble_opengraph_data_for_page(page: Page):
    data = {
        'og:locale': 'en_US',
        'og:site_name': 'Trevor Wagner | Project-Focused Software Engineer, QA Automation',
        'og:title': escape(page.title),
        'og:url': f'https://trevorwagner.dev{page.relative_path}',
        'og:description': escape(page.md_file.page_content[0:300])
    }

    if page.type == 'blogPost':
        data['og:type'] = 'article'
        data['og:image'] = page.blog_post.cover_photo.url
        data['og:image:url'] = page.blog_post.cover_photo.url
        data['og:image:secure_url'] = page.blog_post.cover_photo.url

        data['og:image:width'] = int(page.blog_post.cover_photo.get_attibute_value_for_key('image_height'))
        data['og:image:height'] = int(page.blog_post.cover_photo.get_attibute_value_for_key('image_width'))
        data['og:publish_date'] = timestamp_opengraph_format(page.blog_post.published)

        data['article:published_time'] = timestamp_opengraph_format(page.blog_post.published)

        last_mod = page.blog_post.published \
            if page.blog_post.published > page.blog_post.published \
            else page.md_file.mod_time

        data['article:modified_time'] = data['og:updated_time'] = timestamp_opengraph_format(last_mod)

    else:
        data['og:type'] = 'website'

    return data
