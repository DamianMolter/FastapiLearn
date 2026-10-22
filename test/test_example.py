import pytest

class Student ():
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture
def default_person():
    return Student("John", "Doe", "Computer Science", 3)

def test_person_initialisation(default_person):
    assert default_person.first_name == "John", "First name should be John"
    assert default_person.last_name == "Doe", "Last name should be Doe"
    assert default_person.major == "Computer Science"
    assert default_person.years == 3