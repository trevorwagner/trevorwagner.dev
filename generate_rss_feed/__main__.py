from sqlalchemy.orm import Session
from inventory_service import engine
from inventory_service.models import Page, BlogPost

from generate_rss_feed.builders import build_rss_for_blog_posts
from pathlib import Path

from inventory_service import DIST

rss_xml_file = DIST / "html/blog/feed/rss.xml"
feed_index_php = Path(__file__).parent.resolve() / "../_static/public/feed/index.php"

if __name__ in "__main__":

    with Session(engine) as session:
        blog_posts = (
            session.query(BlogPost).join(Page)
            .order_by(BlogPost.published.desc())
            .all()
        )
        rss = build_rss_for_blog_posts(blog_posts)

    rss_xml_file.parent.mkdir(parents=True, exist_ok=True)

    with open(rss_xml_file, "w") as f:
        f.write(rss)
