from pathlib import Path
from build_html_for_entry import build_html_for_entry
import frontmatter
import json

DIST = Path(__file__).parent.resolve() / '../_dist/'
site_manifest_file = DIST / 'site-manifest.json'

if __name__ in '__main__':
    with open(site_manifest_file) as f:
        manifest = json.load(f)

        for entry in manifest['site']:
            with open(entry['file']['fileName']) as f:
                matter, content = frontmatter.parse(f.read())

                html = build_html_for_entry(entry, matter, content)

                html_file = Path(DIST / 'html/{}index.html'.format(entry['page']['relativePath']))

                parent_folder = Path(html_file.parent)
                if not parent_folder.exists():
                    parent_folder.mkdir(parents=True, exist_ok=True)

                with open(html_file, 'w') as f:
                    f.write(html)
