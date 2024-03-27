from pathlib import Path


def get_page_relative_path(file_path, page_type):
  slug = Path(file_path).stem

  # TODO: Explore updating to match statement once I upgrade to python >= 3.10.
  # TODO: Rewrite this so that it only takes one argument (file_path).
  if page_type == 'blogPost':
    return '/blog/posts/{}/'.format(slug)
  elif slug == 'index':
    return '/'
  else:
    return '/{}/'.format(slug)
