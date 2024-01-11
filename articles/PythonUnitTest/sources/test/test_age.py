from main.age import is_person_older, Person
import pytest


class TestIsPersonOlder:
    @pytest.fixture
    def some_person(self):
        return Person(15, "John", "Doe")

    def test_is_person_older_recognize_a_yound_person(self, some_person):
        assert is_person_older(some_person, 5) is True

    def test_is_person_older_recognize_an_old_person(self, some_person):
        assert is_person_older(some_person, 95) is False
