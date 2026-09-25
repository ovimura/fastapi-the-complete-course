import pytest

def test_equal_or_not_equal():
    assert 1 == 1
    assert 1 != 2

def test_is_instance():
    assert isinstance(1, int)
    assert isinstance('1', str)
    assert not isinstance('1', int)

def test_boolean():
    validate = True
    assert validate is True
    assert ('hello' == 'hello') is True


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


@pytest.fixture
def default_employee():
    return Student(first_name='John', last_name='Doe', major='Computer Science', years=4)




def test_person_initialization(default_employee):
    assert default_employee.first_name == 'John', "First name should be John"
    assert default_employee.last_name == 'Doe', "Last name should be Doe"
    assert default_employee.major == 'Computer Science', "Major should be Computer Science"
    assert default_employee.years == 4, "Years should be 4"
