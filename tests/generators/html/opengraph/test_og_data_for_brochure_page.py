from datetime import datetime
from src.inventory import Page, MDFile

from src.generators.html.opengraph import assemble_opengraph_data_for_page

test_page = Page(
    title="Test Brochure Page Title",
    alt_title="Test Brochure Page Alt Title",
    draft=False,
    type="brochurePage",
    relative_path="/path/to/test/page/",
    md_file_id="999",
    md_file=MDFile(
        _file_path="/path/to/test/page.md",
        mod_time=datetime.now(),
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


def test_og_data_populates_page_type_as_website():
    og_data = assemble_opengraph_data_for_page(test_page)
    result = og_data["og:type"]

    assert result == "website"


def test_og_data_populates_expected_page_description():
    og_data = assemble_opengraph_data_for_page(test_page)
    result = og_data["og:description"]

    assert result == test_page.md_file.page_content[0:300]


def test_og_data_does_not_populate_published_time():
    og_data = assemble_opengraph_data_for_page(test_page)

    assert "article:published_time" not in og_data


def test_og_data_does_not_populate_modified_time():
    og_data = assemble_opengraph_data_for_page(test_page)

    assert "article:modified_time" not in og_data
