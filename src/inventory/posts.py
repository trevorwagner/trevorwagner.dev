from sqlalchemy import asc, desc
from sqlalchemy.orm import Session, joinedload

from src.inventory.models import BlogPost, Page, Image
from src.inventory.db import engine


def list_recent_posts(limit: int, excluding_posts: list[BlogPost]):
    ignored_ids = []

    if excluding_posts is not None:
        ignored_ids.extend(list(map(lambda x: x.id, excluding_posts)))

    with Session(engine) as session:
        matches = (
            session.query(BlogPost)
            .join(Page)
            .options(joinedload(BlogPost.page))
            .options(joinedload(BlogPost.cover_photo).joinedload(Image.variants))
            .filter(Page.draft.is_(False))
            .filter(BlogPost.id.notin_(ignored_ids))
            .order_by(BlogPost.published.desc())
            .all()
        )

        return matches[:limit]


def get_next_post(current_post: BlogPost):
    result = None

    with Session(engine) as session:
        if current_post.id < session.query(BlogPost).count():
            results = (
                session.query(BlogPost)
                .join(Page)
                .options(joinedload(BlogPost.page))
                .filter(Page.draft.is_(False))
                .filter(BlogPost.id > current_post.id)
                .order_by(BlogPost.id.asc())
                .all()
            )

            if len(results) > 0:
                result = results[0]

    return result


def get_previous_post(current_post: BlogPost):
    result = None

    with Session(engine) as session:
        if current_post.id > 1:
            results = (
                session.query(BlogPost)
                .join(Page)
                .options(joinedload(BlogPost.page))
                .filter(Page.draft.is_(False))
                .filter(BlogPost.id < current_post.id)
                .order_by(BlogPost.id.desc())
                .all()
            )

            if len(results) > 0:
                result = results[0]

    return result
