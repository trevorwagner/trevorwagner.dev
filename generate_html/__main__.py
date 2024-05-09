from sqlalchemy.orm import Session

from generate_html.builders import build_html_for_page
from inventory_service import DIST, Page, engine, BlogPost


def save_html_for_page(page: Page, html):
    path = DIST / f'html{page.relative_path}index.html'

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w') as f:
        f.write(html)
    

if __name__ in '__main__':
    with Session(engine) as session:
        # Generate brochure pages
        brochure_pages = session.query(Page).filter(Page.type == 'brochurePage').all()
        for page in brochure_pages:
            html = build_html_for_page(page)
            save_html_for_page(page, html)

        # Generate blog posts
        blog_pages = session.query(Page).join(BlogPost).all()
        for page in blog_pages:
            html = build_html_for_page(page)
            save_html_for_page(page, html)

        # Generate custom pages
        custom_pages = session.query(Page).filter(Page.type == 'custom').all()
        for page in custom_pages:
            html = build_html_for_page(page)
            save_html_for_page(page, html)