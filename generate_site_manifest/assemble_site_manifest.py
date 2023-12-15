import frontmatter
from build_manifest_entry import build_manifest_entry


def assemble_site_manifest(files):
    manifest_entries = []

    for filename in files:
        file_info = {
            'filePath': str(filename),
            'lastMod': filename.stat().st_mtime,
        }

        with open(filename) as f:
            file_info['matter'] = frontmatter.parse(f.read())

        manifest_entries.append(build_manifest_entry(file_info))

    manifest = {"site": manifest_entries}

    return manifest
