import pytest

@pytest.mark.some_random_mark(sanity=True)
@pytest.mark.some_other_mark(bgp=True, client='comcast', order=11)
def test_something():
    assert True
