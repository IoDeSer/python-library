from typing import TextIO, Type

from IoDeSer._DeSer._IoDes import _IoDes
from IoDeSer._DeSer._IoSer import _IoSer


class IoFile:
    @staticmethod
    def write_to_file(obj: object, file: TextIO):
        file.write(IoFile.write_to_string(obj))

    @staticmethod
    def write_to_string(obj: object) -> str:
        return _IoSer.write(obj, 0)

    @staticmethod
    def read_from_file(file: TextIO, object_type: Type) -> object:
        return IoFile.read_from_str(file.read(), object_type)

    @staticmethod
    def read_from_str(ioStr: str, object_type: Type) -> object:
        return _IoDes.read(ioStr, object_type)
