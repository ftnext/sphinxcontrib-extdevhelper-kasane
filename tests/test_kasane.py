from unittest.mock import MagicMock

from sphinx.builders import Builder

from sphinxcontrib.kasane import (
    BuilderFormatCondition,
    MixinDynamicInheritance,
)


class TestMixinDynamicInheritance:
    def test_create_new_class(self) -> None:
        class AwesomeMixin: ...  # NOQA: E701

        class SomeClass: ...  # NOQA: E701

        sut = MixinDynamicInheritance(AwesomeMixin, "AwesomeNewClass")
        actual = sut(SomeClass)

        assert actual.__name__ == "AwesomeNewClass"
        assert issubclass(actual, AwesomeMixin)
        assert issubclass(actual, SomeClass)


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
