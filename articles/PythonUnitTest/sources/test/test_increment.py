from main.increment import increment


def test_increment_should_add_one():
    assert increment(5) == 6
