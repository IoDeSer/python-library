# About
Repository stores code for python library that allows to read from and write to .io file format. Was created using Python 3.7.

## Functions and plans
### Serialization
- [X] Primitive types (int, str)
- [X] Classes
- [X] Sequence subclasses (e.g. list, tuple)
- [X] Combinations of all above
- [ ] Dictionaries
      
### Deserialization
- [X] Primitive types (int, str)
- [X] Classes
- [ ] Sequence subclasses (only type 'list' works)
- [X] Combinations of all above
- [ ] Dictionaries


## Disadvantages
While primitive types or classes with clearly defined types work great with this format, more generic variables such as sequences or maps cause tremendous problems, as their element types are not known.

Because of this, all custom classes that the user wants to serialize or deserialize in the .io file format need to inherit the abstract class 'IoDeserable' and implement the 'io' method, which maps all variable types in a dictionary as follows:
- {"primitive_type": int}
- {"other_class": Class2}
- {"list_type": [int]} (The square brackets ***[]*** indicate that this field is a list, and ***int*** indicates the list element type)

It becomes more understandable after examining the example below.

### Example

```python
from ioDeSer.ioDeSeriable import IoDeSerable
from ioDeSer import ioFile


class Address(IoDeSerable):
    @staticmethod
    def __io__() -> dict:
        return {"city": str, "number": int}

    def __init__(self, city="", number=0):
        self.city = city
        self.number = number

    def __str__(self):
        return f"{self.city} {self.number}"


class Person(IoDeSerable):
    @staticmethod
    def __io__() -> dict:
        return {"name": str, "last_name": str, "age": int, "addresses": [Address]}

    def __init__(self, first_name="", last_name="", age=0, addresses=[]):
        self.name = first_name
        self.last_name = last_name
        self.age = age
        self.addresses = addresses

    def __str__(self):
        return f"{self.name} {self.last_name} {self.age}. " + ' '.join(map(lambda x: '\n\t' + str(x), self.addresses))


person = Person("Jan", "Kowalski", 18, [Address("London", 13), Address("Zurich", 55)])
io = ioFile.write_to_string(person)
print(io)
person = ioFile.read_from_str(io, Person)
print(person)
```
