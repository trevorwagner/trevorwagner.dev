def build_sitemap_for_pages(pages):

    sitemap = "".join(
        [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        ]
    )

    for page in pages:
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
