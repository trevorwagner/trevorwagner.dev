from collect_inventory.analysis.get_page_relative_path import get_page_relative_path


def test_returns_path_within_blog_for_md_file_in_posts():
  path = '/code/trevorwagner.dev/_static/posts/blog_post.md'
  page_type = 'blogPost'
  result = get_page_relative_path(path, page_type)
  assert result == '/blog/posts/blog_post/'


def test_returns_path_within_blog_for_md_file_in_pages():
  path = '/code/trevorwagner.dev/_static/pages/brochure_page_topic.md'
  page_type = ''
  result = get_page_relative_path(path, page_type)
  assert result == '/brochure_page_topic/'


def test_returns_path_within_blog_for_md_file_in_staic_root():
  path = '/code/trevorwagner.dev/_static/index.md'
  page_type = ''
  result = get_page_relative_path(path, page_type)
  assert result == '/'
