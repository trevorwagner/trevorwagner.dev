from pathlib import Path

from sqlalchemy.orm import Session

from src.inventory import engine, DIST, MDFile, Page
from src.generators.xml import build_sitemap_for_pages

xml_sitemap_file = DIST / "html/sitemap.xml"


if __name__ in "__main__":
    with Session(engine) as session:
        pages = (
            session.query(Page).join(MDFile).where(Page.title != "File Not Found").all()
        )
        sitemap = build_sitemap_for_pages(pages)

    xml_sitemap_file.parent.mkdir(parents=True, exist_ok=True)

    with open(xml_sitemap_file, "w") as f:
        f.write(sitemap)
