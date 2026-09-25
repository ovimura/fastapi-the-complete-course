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