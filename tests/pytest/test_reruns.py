import random

import pytest

OS = "Windows"


@pytest.mark.flaky(reruns=3, delay=2)
def test_reruns():
    assert random.choice([True, False])


@pytest.mark.flaky(reruns=3, delay=2)
class TestReruns:
    def test_reruns_1(self):
        assert random.choice([True, False])

    def test_reruns_2(self):
        assert random.choice([True, False])


@pytest.mark.flaky(reruns=3, delay=2, condition=OS == "Windows")
def test_reruns_with_condition():
    assert random.choice([True, False])
