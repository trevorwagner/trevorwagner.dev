from sqlalchemy.orm import Session

from src.generators.html import build_html_for_page
from src.inventory import DIST, Page, engine, BlogPost


def save_content_to_file(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        f.write(content)


if __name__ in "__main__":
    with Session(engine) as session:
        # Generate brochure pages
        brochure_pages = session.query(Page).filter(Page.type == "brochurePage").all()
        for page in brochure_pages:
            html = build_html_for_page(page)
            save_content_to_file(DIST / f"html{page.relative_path}index.html", html)

        # Generate blog posts
        blog_pages = session.query(Page).join(BlogPost).all()
        for page in blog_pages:
            html = build_html_for_page(page)
            save_content_to_file(DIST / f"html{page.relative_path}index.html", html)

        # Generate custom pages (currently /blog/, /content/)
        custom_pages = session.query(Page).filter(Page.type == "custom").all()
        for page in custom_pages:
            html = build_html_for_page(page)

            if page.relative_path == "/contact/":
                save_content_to_file(DIST / f"html{page.relative_path}index.php", html)
            else:
                save_content_to_file(DIST / f"html{page.relative_path}index.html", html)
