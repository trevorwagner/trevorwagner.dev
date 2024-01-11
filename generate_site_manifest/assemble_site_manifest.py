import frontmatter
from .build_manifest_entry import build_manifest_entry
from pathlib import Path

from _static import PAGES_MD


def assemble_site_manifest(files):
    manifest_entries = []

    latest_blog_publish_date = 0

    for filename in files:
        file_info = {
            'filePath': str(filename.resolve()),
            'lastMod': filename.stat().st_mtime,
        }

        with open(filename) as f:
            file_info['matter'] = frontmatter.parse(f.read())

        new_entry = build_manifest_entry(file_info)

        # Keep track of the latest
        if new_entry['page']['type'] == 'blogPost':
            if new_entry['file']['lastMod'] > latest_blog_publish_date:
                latest_blog_publish_date = new_entry['file']['lastMod']

        manifest_entries.append(new_entry)

    blog_home = build_manifest_entry(
        {'filePath': str(Path(PAGES_MD.resolve() / 'blog.md')),
         'lastMod': latest_blog_publish_date
         }
    )

    manifest_entries.append(blog_home)

    manifest = {"site": manifest_entries}

    return manifest
