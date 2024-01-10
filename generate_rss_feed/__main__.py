import json

from .build_rss_from_manifest import build_rss_from_inventory
from pathlib import Path
import shutil

DIST = Path(__file__).parent.resolve() / '../_dist/'
site_manifest_file = DIST / 'site-manifest.json'

rss_xml_file = DIST / 'html/blog/feed/rss.xml'
feed_index_php = Path(__file__).parent.resolve() / '../public/feed/index.php'

if __name__ in '__main__':

    with open(site_manifest_file) as m:
        rss = build_rss_from_inventory(json.load(m))

        parent_folder = Path(rss_xml_file.parent)
        if not parent_folder.exists():
            parent_folder.mkdir(parents=True, exist_ok=True)

        with open(rss_xml_file, 'w') as f:
            f.write(rss)