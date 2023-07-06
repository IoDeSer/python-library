import inspect


class _IoDes:
    @staticmethod
    def read(ioStr, objType):
        ioStr = _IoDes.__substring_brackets(ioStr)
        primitive = (int, str, bool, float)
        # print(objType)

        if objType in primitive:
            obj = objType(ioStr)
        elif objType is list:  # TODO
            ioStr = _IoDes.__delete_tabs(ioStr)
            lst = []
            lines = ioStr.split('\n+\n')
            for i in range(len(lines)):
                lst.append(_IoDes.read(lines[i], str))
                # TODO convert to proper element type, not 'str'
            obj = lst
        elif objType is tuple:
            raise NotImplementedError("TUPLE NOT IMPLEMENTED YET")
        elif inspect.isclass(objType):  # TODO
            try:
                obj = objType()
            except TypeError:
                raise TypeError(
                    "Object of type " + str(objType) + " must have parameterless constructor or with default values.")
            ioStr = _IoDes.__delete_tabs(ioStr)
            fields = vars(obj)

            lines = ioStr.split('\n')
            for l in range(len(lines)):  # TODO fix lines meaby?
                assignments = lines[l].split('->')
                varName = assignments[0].strip()
                foundField = None

                for field in fields:
                    if varName == field:
                        foundField = field
                        break

                if foundField is None:
                    raise NameError(f"Object of type {objType} does not have field named {varName}.")

                if isinstance(fields[foundField], primitive):
                    typeOfElement = type(fields[foundField])
                    val = _IoDes.read(assignments[1].strip(), typeOfElement)
                    setattr(obj, foundField, val)  # TODO was 'field', why?
                else:
                    # TODO add deserialization of classes and lists
                    pass
        else:
            raise NotImplementedError(f"Object of type {objType} is not supported.")
        return obj

    @staticmethod
    def __substring_brackets(ioString):
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

    @staticmethod
    def __delete_tabs(input_str):
        ret = ""
        lines = input_str.split('\n')
        for i in range(len(lines)):
            ret += (lines[i])[1:] + "\n"
        return ret.strip()
