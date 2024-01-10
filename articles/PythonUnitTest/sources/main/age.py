from dataclasses import dataclass

@dataclass
class Person:
    age: int
    first_name: str
    last_name: str

def is_person_older(person : Person, than : int) -> bool:
    return person.age > than

