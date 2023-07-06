import collections.abc
import inspect
from IoDeSer.Errors.TypeErrors import *

class _IoSer:
    @staticmethod
    def __add_shift(shift) -> str:
        ret = ""
        for x in range(shift):
            ret += "\t"
        return ret

    @staticmethod
    def write(obj, shift_number) -> str:
        primitive = (int, str, bool, float)
        ret = ""

        if isinstance(obj, primitive):
            ret = "|" + str(obj) + "|"
        elif isinstance(obj, collections.abc.Sequence):
            arrayRet = ""
            for i in range(len(obj)):
                arrayRet += _IoSer.__add_shift(shift_number + 1) + _IoSer.write(obj[i], shift_number + 1)
                if i < len(obj) - 1:
                    arrayRet += "\n" + _IoSer.__add_shift(shift_number + 1) + "+\n"
            ret = "|\n" + arrayRet + "\n" + _IoSer.__add_shift(shift_number) + "|"
        elif inspect.isclass(obj):
            fields = vars(obj)
            classRet = ""
            first = True

            for field in fields:
                value = fields[field]
                if not first:
                    classRet += "\n"
                first = False
                classRet += _IoSer.__add_shift(shift_number + 1) + field + "->" + _IoSer.write(value, shift_number + 1)
            ret = "|\n" + classRet + "\n" + _IoSer.__add_shift(shift_number) + "|"
        else:
            raise TypeNotSupportedError(type(obj))

        return ret