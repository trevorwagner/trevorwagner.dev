from datetime import datetime

from sqlalchemy.orm import Session

from src.inventory import engine, Page, BlogPost, DIST
from src.generators.xml import build_rss_for_blog_posts, SiteMetadata
from src.generators.dates import timestamp_rfc_822

rss_xml_file = DIST / "html/blog/feed/rss.xml"

if __name__ == "__main__":

    build_time = datetime.now()

    site_metadata = SiteMetadata(
        title="trevorwagner.dev - Blog",
        language="en-us",
        link="https://www.trevorwagner.dev/blog/",
        description="RSS Feed for new blog posts on trevorwagner.dev",
        last_build_date=timestamp_rfc_822(build_time),
        self="https://www.trevorwagner.dev/blog/feed/",
        copyright=f'{build_time.strftime("%Y")} Upstream Consulting LLC. All rights reserved.',
    )

    with Session(engine) as session:
        blog_posts = (
            session.query(BlogPost).join(Page).order_by(BlogPost.published.desc()).all()
        )
        rss = build_rss_for_blog_posts(posts=blog_posts, metadata=site_metadata)

    rss_xml_file.parent.mkdir(parents=True, exist_ok=True)

    with open(rss_xml_file, "w") as f:
        f.write(rss)
