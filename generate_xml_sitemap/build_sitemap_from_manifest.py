from datetime import datetime, timezone


def build_sitemap_from_manifest(manifest):
    sitemap = ''.join([
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ])

    # 2023-12-15T00:20:38.657Z
    for entry in manifest['site']:
        timestamp = (datetime.fromtimestamp(entry['file']['lastMod'], tz=timezone.utc)
                     .strftime('%Y-%m-%dT%H:%M:%S.%fZ'))

        new_item = ''.join([
            '\n\t<url>',
            '\n\t\t<loc>https://www.trevorwagner.dev{}</loc>'.format(entry['page']['relativePath']),
            '\n\t\t<lastmod>{}</lastmod>'.format(timestamp),
            '\n\t</url>'
        ])

        sitemap = ''.join([sitemap, new_item])

    sitemap = ''.join([sitemap, '\n</urlset>'])

    return sitemap
