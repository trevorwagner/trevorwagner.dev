from sqlalchemy.orm import Session

from src.generators.html import build_html_for_page
from src.inventory import DIST, Page, engine, BlogPost
from _static import php_blog_post_query_handler


def save_content_to_file(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        f.write(content)


if __name__ == "__main__":
    with Session(engine) as session:
        # Generate brochure pages
        brochure_pages = (
            session.query(Page)
            .filter(Page.type == "brochurePage")
            .filter(Page.draft == False)
            .all()
        )

        for page in brochure_pages:
            html = build_html_for_page(page)
            save_content_to_file(
                path=DIST / f"html{page.relative_path}index.html", content=html
            )

        # Generate blog post pages
        blog_pages = (
            session.query(Page).join(BlogPost).filter(Page.draft == False).all()
        )

        for page in blog_pages:
            html = build_html_for_page(page)
            save_content_to_file(
                path=DIST / f"html{page.relative_path}index.html", content=html
            )

        # Generate custom pages (currently /blog/, /content/)
        custom_pages = (
            session.query(Page)
            .filter(Page.type == "custom")
            .filter(Page.draft == False)
            .all()
        )

        for page in custom_pages:
            html = build_html_for_page(page)

            if page.relative_path == "/contact/":
                save_content_to_file(DIST / f"html{page.relative_path}index.php", html)
            elif page.relative_path == "/blog/":
                content = php_blog_post_query_handler + "\n\n" + html
                save_content_to_file(
                    DIST / f"html{page.relative_path}index.php", content
                )
            else:
                save_content_to_file(
                    path=DIST / f"html{page.relative_path}index.html", content=html
                )
