from unittest.mock import MagicMock

import pytest
from sphinx.application import Sphinx
from sphinx.builders import Builder

from sphinxcontrib.kasane import (
    BuilderCondition,
    BuilderFormatCondition,
    MixinDynamicInheritance,
    TranslatorSetUp,
)


class TestTranslatorSetUp:
    @pytest.fixture
    def builder(self) -> Builder:
        return MagicMock(spec=Builder)

    @pytest.fixture
    def app(self, builder: Builder) -> Sphinx:
        app = MagicMock(spec=Sphinx)
        app.builder = builder
        return app

    @pytest.fixture
    def unsatisfied_condition(self) -> BuilderCondition:
        condition = MagicMock(spec=BuilderCondition)
        condition.is_satisfied_by.return_value = False
        return condition

    def test_condition_not_satisfied(
        self, app: Sphinx, unsatisfied_condition: BuilderCondition
    ) -> None:
        inheritance = MagicMock(spec=MixinDynamicInheritance)
        sut = TranslatorSetUp(inheritance, unsatisfied_condition)

        sut(app)

        app.set_translator.assert_not_called()  # type: ignore[attr-defined]
        unsatisfied_condition.is_satisfied_by.assert_called_once_with(
            app.builder
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
