import json

from sqlalchemy.orm import Session
from src.inventory import BlogPost, Page, engine, DIST

if __name__ == "__main__":
    blog_posts_json = {"posts": []}

    with Session(engine) as session:
        posts = blog_posts_json["posts"]

        blog_posts = (
            session.query(BlogPost).join(Page).order_by(BlogPost.id.asc()).all()
        )

        for post in blog_posts:
            posts.append(
                {
                    "name": post.page.title,
                    "slug": (
                        post.page.relative_path.split("/")[-2]
                        if post.page.draft == False
                        else ""
                    ),
                }
            )

        with open(DIST / "html/blog/posts/posts.json", "w") as f:
            f.write(json.dumps(blog_posts_json))
