import pytest


def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 2

def test_is_instance():
    assert isinstance("this is a string", str)
    assert not isinstance('3', int)

def test_boolean():
    validated = True
    assert validated is True
    assert ("hello"=="world") is False

def test_type():
    assert type(3) == int
    assert type(3.0) == float
    assert type("world" is not int)

def test_greater_or_less():

    assert 3 > 2
    assert 2 < 3

def test_list():
    num_list = [1, 2, 3, 4, 5]
    any_list = [False, "hello", 3.0, 4]
    assert 3 in num_list
    assert "hello" in any_list
    assert 6 not in num_list


class Student:
    
        def __init__(self, first_name:str, last_name:str, major:str, years:int):
              self.first_name = first_name
              self.last_name = last_name
              self.major = major
              self.years = years


@pytest.fixture
def default_student():
    return Student("John", "Doe", "Computer Science", 3)


def test_person_init(default_student):
    assert default_student.first_name == "John", "First name should be John"
    assert default_student.last_name == "Doe", "Last name should be Doe"
    assert default_student.major == "Computer Science", "Major should be Computer Science"
    assert default_student.years == 3, "Years should be 3"


