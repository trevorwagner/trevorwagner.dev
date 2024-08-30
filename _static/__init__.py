import datetime
import pathlib

static_content = pathlib.Path(__file__).parent.resolve()


# Noted that there definitely appears to be a lot of overlap
# between list_page_files() and list_post_files().
def list_page_files():
    file_list = [static_content / "index.md"]

    for path in pathlib.Path(static_content / "pages/").glob("**/*.md"):
        file_list.append(path)

    return file_list


def list_post_files():
    file_list = []

    for path in pathlib.Path(static_content / "posts/").glob("**/*.md"):
        file_list.append(path)

    return file_list


def get_file_contents(path):
    with open(path) as f:
        return f.read()


def get_file_mod_time(path):
    mod_time = path.stat().st_mtime
    return datetime.datetime.fromtimestamp(mod_time)


php_contact_form_handler = get_file_contents(
    static_content / "assets/contact/form_submission_handler.php"
)
