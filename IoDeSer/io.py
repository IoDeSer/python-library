import collections.abc


class IoFile:
    @staticmethod
    def write_to_file(obj, file):
        file.write(IoFile().__write(obj, 0))

    @staticmethod
    def write_to_string(obj) -> str:
        return IoFile().__write(obj, 0)

    @staticmethod
    def read_from_file(file, type):
        return IoFile().__read(file.read(), type)

    @staticmethod
    def read_from_str(ioStr, type):
        return IoFile().__read(ioStr, type)

    def __add_shift(self, shift) -> str:
        ret = ""
        for x in range(shift):
            ret += "\t"
        return ret

    def __write(self, obj, shift_number) -> str:
        primitive = (int, str, bool, float)
        ret = ""
        if isinstance(obj, primitive):
            ret = "|" + str(obj) + "|"
        elif isinstance(obj, collections.abc.Sequence):
            arrayRet = ""
            for i in range(len(obj)):
                arrayRet += self.__add_shift(shift_number + 1) + self.__write(obj[i], shift_number + 1)
                if i < len(obj) - 1:
                    arrayRet += "\n" + self.__add_shift(shift_number + 1) + "+\n"
            ret = "|\n" + arrayRet + "\n" + self.__add_shift(shift_number) + "|"
        else:  # inspect.isclass(obj):
            fields = vars(obj)
            classRet = ""
            first = True

            for field in fields:
                value = fields[field]
                if not first:
                    classRet += "\n"
                first = False
                classRet += self.__add_shift(shift_number + 1) + field + "->" + self.__write(value, shift_number + 1)
            ret = "|\n" + classRet + "\n" + self.__add_shift(shift_number) + "|"
        return ret

    def __substring_brackets(self, ioString):
        firstIndex = -1
        lastIndex = -1
        for i in range(len(ioString)):
            if ioString[i] == '|':
                firstIndex = i + 1
                break
        for i in range(len(ioString)):
            if ioString[len(ioString) - 1 - i] == '|':
                lastIndex = len(ioString) - 1 - i
                break
        ioString = ioString[firstIndex:lastIndex]
        return ioString

    def __delete_tabs(self, str):
        ret = ""
        lines = str.split('\n')
        for i in range(len(lines)):
            ret += (lines[i])[1:] + "\n"
        return ret.strip()

    def __read(self, ioStr, objType):
        obj = ...
        ioStr = self.__substring_brackets(ioStr)
        primitive = (int, str, bool, float)
        if objType in primitive:
            obj = objType(ioStr)
        elif objType == list:
            ioStr = self.__delete_tabs(ioStr)
            lst = []
            lines = ioStr.split('\n+\n')
            for i in range(len(lines)):
                lst.append(self.__read(lines[i], str))
                # TODO convert to proper element type, not 'str'
            obj = lst
        else:
            try:
                obj = objType()
            except TypeError:
                raise TypeError("Object of type "+str(objType)+" must have parameterless constructor or with default values.")
            ioStr = self.__delete_tabs(ioStr)
            fields = vars(obj)

            lines = ioStr.split('\n')
            for l in range(len(lines)):
                assignments = lines[l].split('->')
                varName = assignments[0].strip()
                foundField=...

                for field in fields:
                    if varName == field:
                        foundField = field
                        break


                if foundField is None:
                    raise NameError("Object of type "+str(objType)+" does not have field named "+varName)

                if isinstance(fields[foundField], primitive):
                    typeOfElement = type(fields[foundField])
                    val = self.__read(assignments[1].strip(), typeOfElement)
                    setattr(obj, field, val)
                    pass
                else:
                    # TODO add deserialization of classes and lists
                    pass

        return obj