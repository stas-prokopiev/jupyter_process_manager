# -*- coding: utf-8 -*-

import pytest
from jupyter_process_manager.skeleton import fib

__author__ = "stanislav"
__copyright__ = "stanislav"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
