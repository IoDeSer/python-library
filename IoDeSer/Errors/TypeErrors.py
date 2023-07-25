from typing import Type


class TypeNotSupportedError(Exception):
    def __init__(self, objectType: Type):
        self._type = objectType
        super().__init__(f"Object of type {self._type} is not supported. Classess must inherit 'IoDeSerable' class.")


class TypeNotImplementedError(Exception):
    def __init__(self, objectType: Type):
        self._type = objectType
        super().__init__(f"Object of type {self._type} is not yet implemented.")
