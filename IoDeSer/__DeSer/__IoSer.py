import collections.abc
import inspect

from IoDeSer.ClassHelper.IoDeSeriable import IoDeSerable
from IoDeSer.Errors.ClassErrors import FieldNotFoundError
from IoDeSer.Errors.TypeErrors import *


class IoSer:
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
                arrayRet += IoSer.__add_shift(shift_number + 1) + IoSer.write(obj[i], shift_number + 1)
                if i < len(obj) - 1:
                    arrayRet += "\n" + IoSer.__add_shift(shift_number + 1) + "+\n"
            ret = "|\n" + arrayRet + "\n" + IoSer.__add_shift(shift_number) + "|"
        elif isinstance(obj, dict):  # TODO dictionary serialization
            raise TypeNotImplementedError(dict)
        elif issubclass(type(obj), IoDeSerable):  # inspect.isclass(type(obj)):
            class_ret = ""
            first = True

            var_types = type(obj).__io__()
            for v in var_types:
                try:
                    value = getattr(obj, v)
                    if not first:
                        class_ret += "\n"
                    first = False
                    class_ret += IoSer.__add_shift(shift_number + 1) + v + "->" + IoSer.write(value,
                                                                                              shift_number + 1)
                except AttributeError:
                    raise FieldNotFoundError(type(obj), v)

            ret = "|\n" + class_ret + "\n" + IoSer.__add_shift(shift_number) + "|"
        else:
            raise TypeNotSupportedError(type(obj))

        return ret
