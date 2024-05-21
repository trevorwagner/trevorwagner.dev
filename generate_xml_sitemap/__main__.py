from pathlib import Path

from sqlalchemy.orm import Session

from inventory_service.models import Page, MDFile
from generate_xml_sitemap.builders import build_sitemap_for_pages
from inventory_service import engine, DIST

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
