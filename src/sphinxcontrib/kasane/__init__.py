import types

from sphinx.builders import Builder

__version__ = "0.0.1"


class MixinDynamicInheritance:
    def __init__(self, mixin_class: type, new_class_name: str) -> None:
        self.mixin_class = mixin_class
        self.new_class_name = new_class_name

    def __call__(self, existing_class: type) -> type:
        return types.new_class(
            self.new_class_name, (self.mixin_class, existing_class), {}
        )


class BuilderFormatCondition:
    def __init__(self, format: str) -> None:
        self.format = format

    def is_satisfied_by(self, builder: Builder) -> bool:
        return builder.format == self.format
