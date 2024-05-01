=======
History
=======

0.6.2 (2024-05-01)
------------------
* Support deeper trees by using iteration instead of recursion.

0.6.1 (2024-04-23)
------------------
* Fixed HTML comment and processing instruction handling.
* Use ``lxml-html-clean`` instead of ``lxml[html_clean]`` in setup.py,
  to avoid https://github.com/jazzband/pip-tools/issues/2004

0.6.0 (2024-04-04)
------------------

* Moved the Git repository to https://github.com/zytedata/html-text.
* Added official support for Python 3.9-3.12.
* Removed support for Python 2.7 and 3.5-3.7.
* Switched the ``lxml`` dependency to ``lxml[html_clean]`` to support
  ``lxml >= 5.2.0``.
* Switch from Travis CI to GitHub Actions.
* CI improvements.

0.5.2 (2020-07-22)
------------------

* Handle lxml Cleaner exceptions (a workaround for
  https://bugs.launchpad.net/lxml/+bug/1838497 );
* Python 3.8 support;
* testing improvements.

0.5.1 (2019-05-27)
------------------

Fixed whitespace handling when ``guess_punct_space`` is False: html-text was
producing unnecessary spaces after newlines.

0.5.0 (2018-11-19)
------------------

Parsel dependency is removed in this release,
though parsel is still supported.

* ``parsel`` package is no longer required to install and use html-text;
* ``html_text.etree_to_text`` function allows to extract text from
  lxml Elements;
* ``html_text.cleaner`` is an ``lxml.html.clean.Cleaner`` instance with
  options tuned for text extraction speed and quality;
* test and documentation improvements;
* Python 3.7 support.

0.4.1 (2018-09-25)
------------------

Fixed a regression in 0.4.0 release: text was empty when
``html_text.extract_text`` is called with a node with text, but
without children.

0.4.0 (2018-09-25)
------------------

This is a backwards-incompatible release: by default html_text functions
now add newlines after elements, if appropriate, to make the extracted text
to look more like how it is rendered in a browser.

To turn it off, pass ``guess_layout=False`` option to html_text functions.

* ``guess_layout`` option to to make extracted text look more like how
  it is rendered in browser.
* Add tests of layout extraction for real webpages.


0.3.0 (2017-10-12)
------------------

* Expose functions that operate on selectors,
  use ``.//text()`` to extract text from selector.


0.2.1 (2017-05-29)
------------------

* Packaging fix (include CHANGES.rst)


0.2.0 (2017-05-29)
------------------

* Fix unwanted joins of words with inline tags: spaces are added for inline
  tags too, but a heuristic is used to preserve punctuation without extra spaces.
* Accept parsed html trees.


0.1.1 (2017-01-16)
------------------

* Travis-CI and codecov.io integrations added


0.1.0 (2016-09-27)
------------------

* First release on PyPI.
