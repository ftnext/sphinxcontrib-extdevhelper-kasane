from unittest.mock import MagicMock

import pytest
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.registry import SphinxComponentRegistry

from sphinxcontrib.kasane import TranslatorSetUp
from sphinxcontrib.kasane.conditions import BuilderCondition
from sphinxcontrib.kasane.inheritance import MixinDynamicInheritance


class TestTranslatorSetUp:
    @pytest.fixture
    def builder(self) -> Builder:
        return MagicMock(spec=Builder)

    @pytest.fixture
    def registry(self) -> SphinxComponentRegistry:
        return MagicMock(spec=SphinxComponentRegistry())

    @pytest.fixture
    def app(
        self, builder: Builder, registry: SphinxComponentRegistry
    ) -> Sphinx:
        app = MagicMock(spec=Sphinx)
        app.builder = builder
        app.registry = registry
        return app

    @pytest.fixture
    def inheritance(self) -> MixinDynamicInheritance:
        return MagicMock(spec=MixinDynamicInheritance(None, ""))

    @pytest.fixture
    def unsatisfied_condition(self) -> BuilderCondition:
        condition = MagicMock(spec=BuilderCondition)
        condition.is_satisfied_by.return_value = False
        return condition

    def test_condition_not_satisfied(
        self,
        app: Sphinx,
        inheritance: MixinDynamicInheritance,
        unsatisfied_condition: BuilderCondition,
    ) -> None:
        sut = TranslatorSetUp(inheritance, unsatisfied_condition)

        sut(app)

        app.set_translator.assert_not_called()  # type: ignore[attr-defined]
        unsatisfied_condition.is_satisfied_by.assert_called_once_with(
            app.builder
        )

    @pytest.fixture
    def satisfied_condition(self) -> BuilderCondition:
        condition = MagicMock(spec=BuilderCondition)
        condition.is_satisfied_by.return_value = True
        return condition

    def test_condition_satisfied(
        self,
        app: Sphinx,
        inheritance: MixinDynamicInheritance,
        satisfied_condition: BuilderCondition,
    ) -> None:
        sut = TranslatorSetUp(inheritance, satisfied_condition)

        sut(app)

        app.registry.get_translator_class.assert_called_once_with(app.builder)  # type: ignore[attr-defined]  # NOQA: E501
        inheritance.assert_called_once_with(
            app.registry.get_translator_class.return_value  # type: ignore[attr-defined]  # NOQA: E501
        )
        app.set_translator.assert_called_once_with(  # type: ignore[attr-defined]  # NOQA: E501
            app.builder.name, inheritance.return_value, override=True
        )
        satisfied_condition.is_satisfied_by.assert_called_once_with(
            app.builder
        )
