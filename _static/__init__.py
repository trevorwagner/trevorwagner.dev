import pathlib

static_content = pathlib.Path(__file__).parent.resolve()


# Noted that there definitely appears to be a lot of overlap
# between these two methods.
def list_page_files():
  file_list = [static_content / "index.md"]

  for path in pathlib.Path(static_content / "pages/").glob('**/*.md'):
    file_list.append(path)

  return file_list


def list_post_files():
  file_list = []

  for path in pathlib.Path(static_content / "posts/").glob('**/*.md'):
    file_list.append(path)

  return file_list
