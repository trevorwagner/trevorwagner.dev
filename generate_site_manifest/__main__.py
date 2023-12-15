from assemble_site_manifest import assemble_site_manifest
from pathlib import Path
from json import dumps

DIST = Path(__file__).parent.resolve() / '../_dist/'
STATIC_CONTENT = Path(__file__).parent.resolve() / '../_static/'

if __name__ in '__main__':
    files = STATIC_CONTENT.glob('**/*.md')

    manifest = assemble_site_manifest(files)

    if not DIST.exists():
        DIST.mkdir(parents=True, exist_ok=True)

    manifest_file = DIST / 'site-manifest.json'
    with open(manifest_file, 'w') as f:
        f.write(dumps(manifest))

