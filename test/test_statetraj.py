# -*- coding: utf-8 -*-
"""
Tests for the statetraj module.

BSD 3-Clause License
Copyright (c) 2019-2020, Daniel Nagel
All rights reserved.

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np
import pytest
from numpy import array, int32

from msmhelper.statetraj import StateTraj


@pytest.fixture
def index_traj():
    """Define index trajectory."""
    traj = array(
        [0, 0, 0, 1, 1, 1, 2, 2, 2, 1, 1, 1, 0, 2, 1, 2, 2, 2],
        dtype=int32,
    )
    return StateTraj(traj)


@pytest.fixture
def state_traj():
    """Define state trajectory."""
    traj = array(
        [0, 0, 0, 3, 3, 3, 2, 2, 2, 3, 3, 3, 0, 2, 3, 2, 2, 2],
        dtype=int32,
    )
    return StateTraj(traj)


# ~~~ TESTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def test_StateTraj_constructor(state_traj):
    """Test construction of object."""
    assert state_traj is StateTraj(state_traj)
    np.testing.assert_array_equal(
        state_traj.trajs,
        StateTraj(state_traj.state_trajs).trajs,
    )


def test_nstates(state_traj):
    """Test nstates property."""
    assert state_traj.nstates == len(np.unique(state_traj[0]))

    with pytest.raises(AttributeError):
        state_traj.nstates = 5


def test_ntrajs(state_traj):
    """Test ntrajs property."""
    assert state_traj.ntrajs == len(state_traj.trajs)

    with pytest.raises(AttributeError):
        state_traj.ntrajs = 5


def test_index_trajs(state_traj, index_traj):
    """Test index trajs property."""
    np.testing.assert_array_equal(
        index_traj.trajs,
        index_traj.state_trajs,
    )
    np.testing.assert_array_equal(
        state_traj.trajs,
        state_traj.index_trajs,
    )

    with pytest.raises(AttributeError):
        state_traj.trajs = 5
    with pytest.raises(AttributeError):
        state_traj.index_trajs = 5


def test___eq__(state_traj, index_traj):
    """Test eq method."""
    for traj in [state_traj, index_traj]:
        assert StateTraj(traj.state_trajs) == traj

    assert state_traj != index_traj
    assert state_traj != 5


def test___repr__(state_traj, index_traj):
    """Test repr method."""
    for traj in [state_traj, index_traj]:
        assert eval(traj.__repr__()) == traj  # noqa: S307


def test___str__(state_traj, index_traj):
    """Test str method."""
    for traj in [state_traj, index_traj]:
        assert traj.__str__().startswith('[')


def test_as_list(state_traj, index_traj):
    """Test iterating over object."""
    for traj in [state_traj, index_traj]:
        for trajectory in traj:
            assert StateTraj(trajectory) == traj