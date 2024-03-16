from __future__ import annotations

import types

from sphinx.application import Sphinx

from sphinxcontrib.kasane.conditions import BuilderCondition

__version__ = "0.0.1"


class TranslatorSetUp:
    def __init__(
        self, inheritance: MixinDynamicInheritance, condition: BuilderCondition
    ) -> None:
        self.inheritance = inheritance
        self.condition = condition

    def __call__(self, app: Sphinx) -> None:
        if not self.condition.is_satisfied_by(app.builder):
            return

        builder = app.builder
        translator_class = app.registry.get_translator_class(builder)
        app.set_translator(
            builder.name, self.inheritance(translator_class), override=True
        )


class MixinDynamicInheritance:
    def __init__(self, mixin_class: type, new_class_name: str) -> None:
        self.mixin_class = mixin_class
        self.new_class_name = new_class_name

    def __call__(self, existing_class: type) -> type:
        return types.new_class(
            self.new_class_name, (self.mixin_class, existing_class), {}
        )
