============
HTML to Text
============


.. image:: https://img.shields.io/pypi/v/html-text.svg
   :target: https://pypi.python.org/pypi/html-text
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/html-text.svg
   :target: https://pypi.python.org/pypi/html-text
   :alt: Supported Python Versions

.. image:: https://github.com/zytedata/html-text/workflows/tox/badge.svg
   :target: https://github.com/zytedata/html-text/actions
   :alt: Build Status

.. image:: https://codecov.io/github/zytedata/html-text/coverage.svg?branch=master
   :target: https://codecov.io/gh/zytedata/html-text
   :alt: Coverage report

Extract text from HTML

* Free software: MIT license

How is html_text different from ``.xpath('//text()')`` from LXML
or ``.get_text()`` from Beautiful Soup?

* Text extracted with ``html_text`` does not contain inline styles,
  javascript, comments and other text that is not normally visible to users;
* ``html_text`` normalizes whitespace, but in a way smarter than
  ``.xpath('normalize-space())``, adding spaces around inline elements
  (which are often used as block elements in html markup), and trying to
  avoid adding extra spaces for punctuation;
* ``html-text`` can add newlines (e.g. after headers or paragraphs), so
  that the output text looks more like how it is rendered in browsers.

Install
-------

Install with pip::

    pip install html-text

The package depends on lxml, so you might need to install additional
packages: http://lxml.de/installation.html


Usage
-----

Extract text from HTML::

    >>> import html_text
    >>> html_text.extract_text('<h1>Hello</h1> world!')
    'Hello\n\nworld!'

    >>> html_text.extract_text('<h1>Hello</h1> world!', guess_layout=False)
    'Hello world!'

Passed html is first cleaned from invisible non-text content such
as styles, and then text is extracted.

You can also pass an already parsed ``lxml.html.HtmlElement``:

    >>> import html_text
    >>> tree = html_text.parse_html('<h1>Hello</h1> world!')
    >>> html_text.extract_text(tree)
    'Hello\n\nworld!'

If you want, you can handle cleaning manually; use lower-level
``html_text.etree_to_text`` in this case:

    >>> import html_text
    >>> tree = html_text.parse_html('<h1>Hello<style>.foo{}</style>!</h1>')
    >>> cleaned_tree = html_text.cleaner.clean_html(tree)
    >>> html_text.etree_to_text(cleaned_tree)
    'Hello!'

parsel.Selector objects are also supported; you can define
a parsel.Selector to extract text only from specific elements:

    >>> import html_text
    >>> sel = html_text.cleaned_selector('<h1>Hello</h1> world!')
    >>> subsel = sel.xpath('//h1')
    >>> html_text.selector_to_text(subsel)
    'Hello'

NB parsel.Selector objects are not cleaned automatically, you need to call
``html_text.cleaned_selector`` first.

Main functions and objects:

* ``html_text.extract_text`` accepts html and returns extracted text.
* ``html_text.etree_to_text`` accepts parsed lxml Element and returns
  extracted text; it is a lower-level function, cleaning is not handled
  here.
* ``html_text.cleaner`` is an ``lxml.html.clean.Cleaner`` instance which
  can be used with ``html_text.etree_to_text``; its options are tuned for
  speed and text extraction quality.
* ``html_text.cleaned_selector`` accepts html as text or as
  ``lxml.html.HtmlElement``, and returns cleaned ``parsel.Selector``.
* ``html_text.selector_to_text`` accepts ``parsel.Selector`` and returns
  extracted text.

If ``guess_layout`` is True (default), a newline is added before and after
``newline_tags``, and two newlines are added before and after
``double_newline_tags``. This heuristic makes the extracted text
more similar to how it is rendered in the browser. Default newline and double
newline tags can be found in `html_text.NEWLINE_TAGS`
and `html_text.DOUBLE_NEWLINE_TAGS`.

It is possible to customize how newlines are added, using ``newline_tags`` and
``double_newline_tags`` arguments (which are `html_text.NEWLINE_TAGS` and
`html_text.DOUBLE_NEWLINE_TAGS` by default). For example, don't add a newline
after ``<div>`` tags:

    >>> newline_tags = html_text.NEWLINE_TAGS - {'div'}
    >>> html_text.extract_text('<div>Hello</div> world!',
    ...                        newline_tags=newline_tags)
    'Hello world!'

Apart from just getting text from the page (e.g. for display or search),
one intended usage of this library is for machine learning (feature extraction).
If you want to use the text of the html page as a feature (e.g. for classification),
this library gives you plain text that you can later feed into a standard text
classification pipeline.
If you feel that you need html structure as well, check out
`webstruct <http://webstruct.readthedocs.io/en/latest/>`_ library.
