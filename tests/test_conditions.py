from unittest.mock import MagicMock

from sphinx.builders import Builder

from sphinxcontrib.kasane.conditions import BuilderFormatCondition


class TestBuilderFormatCondition:
    def test_satisfied(self):
        html_format_builder = MagicMock(spec=Builder)
        html_format_builder.format = "html"

        sut = BuilderFormatCondition("html")

        assert sut.is_satisfied_by(html_format_builder)

    def test_not_satisfied(self):
        not_html_format_builder = MagicMock(spec=Builder)
        not_html_format_builder.format = "text"

        sut = BuilderFormatCondition("html")

        assert not sut.is_satisfied_by(not_html_format_builder)
