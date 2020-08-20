# -*- coding: utf-8 -*-
"""Tests for the decorators module.

BSD 3-Clause License
Copyright (c) 2019-2020, Daniel Nagel
All rights reserved.

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import warnings

import pytest

from msmhelper import decorators


# ~~~ TESTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_deprecated():
    """Test deprecated warning."""
    # define function
    kwargs = {'msg': 'msg', 'since': '1.0.0', 'remove': '1.2.0'}
    @decorators.deprecated(**kwargs)
    def func():
        return True

    warning_msg = (
        'Calling deprecated function func. {msg}'.format(**kwargs) +
        ' -- Deprecated since version {since}'.format(**kwargs) +
        ' -- Function will be removed starting from {remove}'.format(**kwargs)
    )

    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            assert func()
        except DeprecationWarning as dw:
            assert str(dw) == warning_msg
        else:
            raise AssertionError()


def test_shortcut():
    """Test shortcut warning."""
    # test for function
    @decorators.shortcut('f')
    def func():
        pass

    try:
        f()
    except NameError:
        raise AssertionError()
