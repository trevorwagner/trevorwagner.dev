from pathlib import Path
from re import match


def get_page_relative_path(file_path, page_type):
    slug = Path(file_path).stem

    # TODO: Explore updating to match statement once I upgrade to python >= 3.10.
    # TODO: Rewrite this so that it only takes one argument (file_path).
    if page_type == "blogPost":
        return f"/blog/posts/{slug}/"
    elif slug == "index":
        return "/"
    else:
        return "/{}/".format(slug)


def get_page_type(file_path):
    f = ""
    page_type = ""

    try:
        f = match(r".*/_static/(.*)/", str(file_path)).group(1)
    except:
        f = "/"

    if f == "posts":
        page_type = "blogPost"
    elif f == "pages" or f == "/":
        page_type = "brochurePage"
    else:
        page_type = "custom"

    return page_type
