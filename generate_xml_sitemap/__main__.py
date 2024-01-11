from pathlib import Path
import json
from .build_sitemap_from_manifest import build_sitemap_from_manifest

DIST = Path(__file__).parent.resolve() / '../_dist/'
site_manifest_file = DIST / 'site-manifest.json'

xml_sitemap_file = DIST / 'html/sitemap.xml'


if __name__ in '__main__':
    with open(site_manifest_file) as m:
        sitemap = build_sitemap_from_manifest(json.load(m))

        parent_folder = Path(xml_sitemap_file.parent)
        if not parent_folder.exists():
            parent_folder.mkdir(parents=True, exist_ok=True)

        with open(xml_sitemap_file, 'w') as f:
            f.write(sitemap)
