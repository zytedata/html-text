from __future__ import annotations

from pathlib import Path

import lxml.html
import pytest

from html_text import (
    DOUBLE_NEWLINE_TAGS,
    NEWLINE_TAGS,
    cleaned_selector,
    cleaner,
    etree_to_text,
    extract_text,
    parse_html,
    selector_to_text,
)

ROOT = Path(__file__).parent


@pytest.fixture(
    params=[
        {"guess_punct_space": True, "guess_layout": False},
        {"guess_punct_space": False, "guess_layout": False},
        {"guess_punct_space": True, "guess_layout": True},
        {"guess_punct_space": False, "guess_layout": True},
    ]
)
def all_options(request):
    return request.param


def test_extract_no_text_html(all_options):
    html = (
        '<!DOCTYPE html><html><body><p><video width="320" height="240" '
        'controls><source src="movie.mp4" type="video/mp4"><source '
        'src="movie.ogg" type="video/ogg"></video></p></body></html>'
    )
    assert extract_text(html, **all_options) == ""


def test_extract_text(all_options):
    html = "<html><style>.div {}</style><body><p>Hello,   world!</body></html>"
    assert extract_text(html, **all_options) == "Hello, world!"


def test_declared_encoding(all_options):
    html = (
        '<?xml version="1.0" encoding="utf-8" ?>'
        "<html><style>.div {}</style>"
        "<body>Hello,   world!</p></body></html>"
    )
    assert extract_text(html, **all_options) == "Hello, world!"


def test_empty(all_options):
    assert extract_text("", **all_options) == ""
    assert extract_text(" ", **all_options) == ""
    assert extract_text(None, **all_options) == ""


def test_comment(all_options):
    assert extract_text("<!-- hello world -->", **all_options) == ""


def test_comment_fragment(all_options):
    node = lxml.html.fragment_fromstring("<!-- hello world -->")
    assert extract_text(node, **all_options) == ""


def test_processing_instruction(all_options):
    assert extract_text('<?dbfo label-width="width"?>', **all_options) == ""


def test_processing_instruction_fragment(all_options):
    node = lxml.html.fragment_fromstring('<?dbfo label-width="width"?>')
    assert extract_text(node, **all_options) == ""


def test_extract_text_from_tree(all_options):
    html = "<html><style>.div {}</style><body><p>Hello,   world!</body></html>"
    tree = parse_html(html)
    assert extract_text(tree, **all_options) == "Hello, world!"


def test_extract_text_from_node(all_options):
    html = "<html><style>.div {}</style><body><p>Hello,   world!</p></body></html>"
    tree = parse_html(html)
    node = tree.xpath("//p")[0]
    assert extract_text(node, **all_options) == "Hello, world!"


def test_inline_tags_whitespace(all_options):
    html = "<span>field</span><span>value  of</span><span></span>"
    assert extract_text(html, **all_options) == "field value of"


def test_extract_text_from_fail_html():
    html = "<html><frameset><frame></frameset></html>"
    tree = parse_html(html)
    node = tree.xpath("/html/frameset")[0]
    assert extract_text(node) == ""


def test_punct_whitespace():
    html = "<div><span>field</span>, and more</div>"
    assert extract_text(html, guess_punct_space=False) == "field , and more"
    assert extract_text(html, guess_punct_space=True) == "field, and more"


def test_punct_whitespace_preserved():
    html = (
        "<div><span>по</span><span>ле</span>, and  ,  "
        "<span>more </span>!<span>now</div>a (<b>boo</b>)"
    )
    text = extract_text(html, guess_punct_space=True, guess_layout=False)
    assert text == "по ле, and , more ! now a (boo)"


@pytest.mark.xfail(reason="code punctuation should be handled differently")
def test_bad_punct_whitespace():
    html = (
        "<pre><span>trees</span> "
        "<span>=</span> <span>webstruct</span>"
        "<span>.</span><span>load_trees</span>"
        "<span>(</span><span>&quot;train/*.html&quot;</span>"
        "<span>)</span></pre>"
    )
    text = extract_text(html, guess_punct_space=False, guess_layout=False)
    assert text == 'trees = webstruct . load_trees ( "train/*.html" )'

    text = extract_text(html, guess_punct_space=True, guess_layout=False)
    assert text == 'trees = webstruct.load_trees("train/*.html")'


def test_selectors(all_options):
    pytest.importorskip("parsel")
    html = (
        '<span><span id="extract-me">text<a>more</a>'
        "</span>and more text <a> and some more</a> <a></a> </span>"
    )
    # Selector
    sel = cleaned_selector(html)
    assert (
        selector_to_text(sel, **all_options) == "text more and more text and some more"
    )

    # SelectorList
    subsel = sel.xpath('//span[@id="extract-me"]')
    assert selector_to_text(subsel, **all_options) == "text more"
    subsel = sel.xpath("//a")
    assert selector_to_text(subsel, **all_options) == "more and some more"
    subsel = sel.xpath('//a[@id="extract-me"]')
    assert selector_to_text(subsel, **all_options) == ""
    subsel = sel.xpath("//foo")
    assert selector_to_text(subsel, **all_options) == ""


def test_nbsp():
    html = "<h1>Foo&nbsp;Bar</h1>"
    assert extract_text(html) == "Foo Bar"


def test_guess_layout():
    html = (
        "<title>  title  </title><div>text_1.<p>text_2 text_3</p>"
        '<p id="demo"></p><ul><li>text_4</li><li>text_5</li></ul>'
        "<p>text_6<em>text_7</em>text_8</p>text_9</div>"
        '<script>document.getElementById("demo").innerHTML = '
        '"This should be skipped";</script> <p>...text_10</p>'
    )

    text = (
        "title text_1. text_2 text_3 text_4 text_5 text_6 text_7 "
        "text_8 text_9 ...text_10"
    )
    assert extract_text(html, guess_punct_space=False, guess_layout=False) == text

    text = (
        "title\n\ntext_1.\n\ntext_2 text_3\n\ntext_4\ntext_5"
        "\n\ntext_6 text_7 text_8\n\ntext_9\n\n...text_10"
    )
    assert extract_text(html, guess_punct_space=False, guess_layout=True) == text

    text = (
        "title text_1. text_2 text_3 text_4 text_5 text_6 text_7 "
        "text_8 text_9...text_10"
    )
    assert extract_text(html, guess_punct_space=True, guess_layout=False) == text

    text = (
        "title\n\ntext_1.\n\ntext_2 text_3\n\ntext_4\ntext_5\n\n"
        "text_6 text_7 text_8\n\ntext_9\n\n...text_10"
    )
    assert extract_text(html, guess_punct_space=True, guess_layout=True) == text


def test_basic_newline():
    html = "<div>a</div><div>b</div>"
    assert extract_text(html, guess_punct_space=False, guess_layout=False) == "a b"
    assert extract_text(html, guess_punct_space=False, guess_layout=True) == "a\nb"
    assert extract_text(html, guess_punct_space=True, guess_layout=False) == "a b"
    assert extract_text(html, guess_punct_space=True, guess_layout=True) == "a\nb"


def test_adjust_newline():
    html = "<div>text 1</div><p><div>text 2</div></p>"
    assert extract_text(html, guess_layout=True) == "text 1\n\ntext 2"


def test_personalize_newlines_sets():
    html = (
        "<span><span>text<a>more</a>"
        "</span>and more text <a> and some more</a> <a></a> </span>"
    )

    text = extract_text(html, guess_layout=True, newline_tags=NEWLINE_TAGS | {"a"})
    assert text == "text\nmore\nand more text\nand some more"

    text = extract_text(
        html, guess_layout=True, double_newline_tags=DOUBLE_NEWLINE_TAGS | {"a"}
    )
    assert text == "text\n\nmore\n\nand more text\n\nand some more"


def _webpage_paths() -> list[tuple[Path, Path]]:
    webpages = sorted((ROOT / "test_webpages").glob("*.html"))
    extracted = sorted((ROOT / "test_webpages").glob("*.txt"))
    return list(zip(webpages, extracted))


@pytest.mark.parametrize(("page", "extracted"), _webpage_paths())
def test_webpages(page, extracted):
    html = page.read_text(encoding="utf-8")
    expected = extracted.read_text(encoding="utf-8")
    assert extract_text(html) == expected

    tree = cleaner.clean_html(parse_html(html))
    assert etree_to_text(tree) == expected


def test_deep_html():
    """Make sure we don't crash due to recursion limit."""
    # Build a deep tree manually as default parser would only allow
    # for 255 depth, but deeper trees are possible with other parsers
    n = 5000
    parent = root = None
    for _ in range(n):
        el = lxml.html.Element("div")
        el.text = "foo"
        if parent is None:
            root = el
            parent = el
        else:
            parent.append(el)
            parent = el

    assert extract_text(root) == ("foo\n" * n).strip()
