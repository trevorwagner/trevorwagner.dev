from xml.sax.saxutils import escape

from src.inventory import Page
from src.generators.dates.timestamps import timestamp_opengraph_format


def assemble_opengraph_data_for_page(page: Page):
    data = {
        "og:locale": "en_US",
        "og:site_name": "Trevor Wagner | Project-Focused Software Engineer, QA Automation",
        "og:title": escape(page.title),
        "og:url": f"https://www.trevorwagner.dev{page.relative_path}",
        "og:description": escape(page.prepared_content[0:300]),
    }

    if page.type == "blogPost":
        use_cover_photo = page.blog_post.cover_photo.variants[0]

        data["og:type"] = "article"
        data["og:image"] = use_cover_photo.url
        data["og:image:url"] = use_cover_photo.url
        data["og:image:secure_url"] = use_cover_photo.url

        data["og:image:width"] = use_cover_photo.width
        data["og:image:height"] = use_cover_photo.height
        data["og:publish_date"] = timestamp_opengraph_format(page.blog_post.published)

        data["article:published_time"] = timestamp_opengraph_format(
            page.blog_post.published
        )

        last_mod = (
            page.blog_post.published
            if page.blog_post.published > page.blog_post.published
            else page.md_file.mod_time
        )

        data["article:modified_time"] = data["og:updated_time"] = (
            timestamp_opengraph_format(last_mod)
        )

    else:
        data["og:type"] = "website"

    return data
