from src.analysis.md_files import get_page_type


def test_returns_blog_post_for_file_in_posts():
    path = "/code/trevorwagner.dev/_static/posts/blog_post.md"
    result = get_page_type(path)
    assert result == "blogPost"


def test_returns_page_for_file_in_pages():
    path = "/code/trevorwagner.dev/_static/pages/blog_post.md"
    result = get_page_type(path)
    assert result == "brochurePage"


def test_returns_custom_for_file_in_neither_pages_nor_posts():
    path = "/code/trevorwagner.dev/_static/something_fancy/blog_post.md"
    result = get_page_type(path)
    assert result == "custom"


def test_returns_brochure_page_for_file_at_static_root():
    path = "/code/trevorwagner.dev/index.md"
    result = get_page_type(path)
    assert result == "brochurePage"
