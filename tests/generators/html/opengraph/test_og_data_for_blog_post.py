from datetime import datetime
from src.inventory import Page, MDFile, BlogPost, Image, ImageVariant

from src.generators.html.opengraph import assemble_opengraph_data_for_page

test_page = Page(
    title="Test Blog Post Title",
    alt_title="Test Blog Post Alt Title",
    draft=False,
    type="blogPost",
    relative_path="/path/to/test/page/",
    blog_post=BlogPost(
        published=datetime.fromisoformat("2023-06-24T22:14:00-05:00"),
        cover_photo=Image(
            name="trevorwagner/test/photo",
            variants=[
                ImageVariant(
                    width=600,
                    height=800,
                    mime_type="image/jpeg",
                    length="1010101",
                    url="https://static.example.com/images/trevorwagner/test/photo/800x600.jpg",
                ),
                ImageVariant(
                    width=1024,
                    height=768,
                    mime_type="image/jpeg",
                    length="2020202",
                    url="https://static.example.com/images/trevorwagner/test/photo/1024x768.jpg",
                ),
            ],
        ),
    ),
    md_file_id="999",
    md_file=MDFile(
        _file_path="/path/to/test/page.md",
        mod_time=datetime.fromisoformat("2024-06-24T14:14:48-05:00"),
        page_content="Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        + "Integer semper dolor nec dui posuere facilisis. Curabitur tempus posuere "
        + "nunc, sed porttitor arcu cursus id. Nam dolor ipsum, aliquam ut magna "
        + "tristique, elementum faucibus mauris. Nullam tempor tortor sit amet "
        + "pellentesque rutrum. Nulla dignissim fermentum hendrerit.",
    ),
)


def test_og_data_populates_expected_locale():
    og_data = assemble_opengraph_data_for_page(test_page)
    result = og_data["og:locale"]

    assert result == "en_US"


def test_og_data_populates_expected_site_name():
    og_data = assemble_opengraph_data_for_page(test_page)
    result = og_data["og:site_name"]

    assert result == "Trevor Wagner | Project-Focused Software Engineer, QA Automation"


def test_og_data_populates_expected_page_url():
    og_data = assemble_opengraph_data_for_page(test_page)
    result = og_data["og:url"]

    assert result == f"https://www.trevorwagner.dev{test_page.relative_path}"


def test_og_data_populates_title():
    og_data = assemble_opengraph_data_for_page(test_page)
    result = og_data["og:title"]

    assert result == test_page.title


def test_og_data_populates_page_description_length():
    og_data = assemble_opengraph_data_for_page(test_page)
    result = og_data["og:description"]

    assert len(result) == 300


def test_og_data_populates_page_type_as_article():
    og_data = assemble_opengraph_data_for_page(test_page)
    result = og_data["og:type"]

    assert result == "article"


def test_og_data_populates_expected_page_description():
    og_data = assemble_opengraph_data_for_page(test_page)
    result = og_data["og:description"]

    assert result == test_page.md_file.page_content[0:300]


def test_og_data_populates_expected_page_published_time():
    og_data = assemble_opengraph_data_for_page(test_page)
    result = og_data["article:published_time"]

    assert result == "2023-06-24T22:14:00-05:00"


def test_og_data_populates_expected_page_modified_time():
    og_data = assemble_opengraph_data_for_page(test_page)
    result = og_data["article:modified_time"]

    assert result == "2024-06-24T14:14:48-05:00"
