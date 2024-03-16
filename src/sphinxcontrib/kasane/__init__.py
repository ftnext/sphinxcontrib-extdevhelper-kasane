from __future__ import annotations

import types
from typing import Protocol

from sphinx.application import Sphinx
from sphinx.builders import Builder

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

        builder_name = app.builder.name
        if translator_class := app.registry.translators.get(builder_name):
            app.set_translator(
                builder_name, self.inheritance(translator_class), override=True
            )
        else:
            app.set_translator(
                builder_name,
                self.inheritance(app.builder.default_translator_class),
            )


class MixinDynamicInheritance:
    def __init__(self, mixin_class: type, new_class_name: str) -> None:
        self.mixin_class = mixin_class
        self.new_class_name = new_class_name

    def __call__(self, existing_class: type) -> type:
        return types.new_class(
            self.new_class_name, (self.mixin_class, existing_class), {}
        )


class BuilderCondition(Protocol):
    def is_satisfied_by(self, builder: Builder) -> bool: ...


class BuilderFormatCondition:
    def __init__(self, format: str) -> None:
        self.format = format

    def is_satisfied_by(self, builder: Builder) -> bool:
        return builder.format == self.format
