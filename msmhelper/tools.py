# -*- coding: utf-8 -*-
"""Set of helpful functions.

BSD 3-Clause License
Copyright (c) 2019-2020, Daniel Nagel
All rights reserved.

TODO:
    - Correct border effects of running mean

"""
# ~~~ IMPORT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import datetime
import getpass  # get user name with getpass.getuser()
import os
import platform  # get pc name with platform.node()
import sys

import numpy as np

import __main__ as main


# ~~~ FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def shift_data(array, val_old, val_new, dtype=np.int32):
    """Shift integer array (data) from old to new values.

    > **CAUTION:**
    > The values of `val_old`, `val_new` and `data` needs to be integers.

    The basic function is based on Ashwini_Chaudhary solution:
    https://stackoverflow.com/a/29408060

    Parameters
    ----------
    array : ndarray, list, list of ndarrays
        1D data or a list of data.

    val_old : ndarray or list
        Values in data which should be replaced. All values needs to be within
        the range of `[data.min(), data.max()]`

    val_new : ndarray or list
        Values which will be used instead of old ones.

    dtype : data-type, optional
        The desired data-type. Needs to be of type unsigned integer.

    Returns
    -------
    array : ndarray
        Shifted data in same shape as input.

    """
    # check data-type
    if not np.issubdtype(dtype, np.integer):
        raise TypeError('An unsigned integer type is needed.')

    # flatten data
    array, shape_kwargs = _flatten_data(array)

    # offset data and val_old to allow negative values
    offset = np.min([np.min(array), np.min(val_new)])

    # convert to np.array
    val_old = (np.asarray(val_old) - offset).astype(dtype)
    val_new = (np.asarray(val_new) - offset).astype(dtype)

    # convert data and shift
    array = (array - offset).astype(dtype)

    # shift data
    conv = np.arange(array.max() + 1, dtype=dtype)
    conv[val_old] = val_new
    array = conv[array]

    # shift data back
    array = array.astype(np.int32) + offset

    # reshape and return
    return _unflatten_data(array, shape_kwargs)


def rename_by_population(traj, return_permutation=False):
    r"""Rename states sorted by their population starting from 1.

    Parameters
    ----------
    traj : ndarray, list of ndarrays
        State trajectory or list of state trajectories.

    return_permutation : bool
        Return additionaly the permutation to achieve performed renaming.
        Default is False.

    Returns
    -------
    traj : ndarray
        Renamed data.

    permutation : ndarray
        Permutation going from old to new state nameing. So the `i`th state
        of the new naming corresponds to the old state `permutation[i-1]`.

    """
    # get unique states with population
    states, pop = np.unique(traj, return_counts=True)

    # get decreasing order
    idx_sort = np.argsort(pop)[::-1]

    # rename states
    traj_renamed = shift_data(
        traj,
        val_old=states[idx_sort],
        val_new=np.arange(len(states)) + 1,
    )
    if return_permutation:
        return traj_renamed, states[idx_sort]
    return traj_renamed


def runningmean(array, window):
    r"""Compute centered running average with given window size.

    This function returns the centered based running average of the given
    data. The output of this function is of the same length as the input,
    by assuming that the given data is zero before and after the given
    series. Hence, there are border affects which are not corrected.

    > **CAUTION:**
    > If the given window is even (not symmetric) it will be shifted towards
    > the beginning of the current value. So for `window=4`, it will consider
    > the current position \(i\), the two to the left \(i-2\) and \(i-1\) and
    > one to the right \(i+1\).

    Function is taken from lapis:
    https://stackoverflow.com/questions/13728392/moving-average-or-running-mean

    Parameters
    ----------
    array : ndarray
        One dimensional numpy array.

    window : int
        Integer which specifies window-width.

    Returns
    -------
    array_rmean : ndarray
        Data which is time-averaged over the specified window.

    """
    # Calculate running mean
    return np.convolve(
        array,
        np.ones(window) / window,
        mode='same',
    )


def swapcols(array, indicesold, indicesnew):
    r"""Interchange cols of an ndarray.

    This method swaps the specified columns.
    .. todo:: Optimize memory usage

    Parameters
    ----------
    array : ndarray
        2D numpy array.
    indicesold : integer or ndarray
        1D array of indices.
    indicesnew : integer or ndarray
        1D array of new indices

    Returns
    -------
    array_swapped : ndarray
        2D numpy array with swappend columns.

    """
    # cast to 1d arrays
    indicesnew = _asindex(indicesnew)
    indicesold = _asindex(indicesold)

    if len(indicesnew) != len(indicesold):
        raise ValueError('Indices needs to be of same shape.')

    # cast data
    array = np.asarray(array)

    if np.all(indicesnew == indicesold):
        return array

    # array.T[indicesold] = array.T[indicesnew] fails for large datasets
    array_swapped = np.copy(array)
    array_swapped.T[indicesold] = array.T[indicesnew]

    return array_swapped


def get_runtime_user_information():
    r"""Get user runtime information.

    > **CAUTION:**
    > For python 3.5 or lower the date is not formatted and contains
    > microscends.

    Returns
    -------
    RUI : dict
        Holding username in 'user', pc name in 'pc', date of execution 'date',
        path of execution 'script_dir' and name of execution main file
        'script_name'. In case of interactive usage, script_name is 'console'.

    """
    try:
        script_dir, script_name = os.path.split(
            os.path.abspath(main.__file__),  # noqa: WPS609
        )
    except AttributeError:
        script_dir, script_name = '', 'console'

    # get time without microseconds
    date = datetime.datetime.now()
    if sys.version_info >= (3, 6):
        date = date.isoformat(sep=' ', timespec='seconds')

    return {
        'user': getpass.getuser(),
        'pc': platform.node(),
        'date': date,
        'script_dir': script_dir,
        'script_name': script_name,
    }


def _asindex(idx):
    """Cast to 1d integer ndarray."""
    idx = np.atleast_1d(idx).astype(np.int64)
    if len(idx.shape) > 1:
        raise ValueError('Wrong dimensionality of indices.')
    return idx


def _check_quadratic(matrix):
    """Check if matrix is quadratic."""
    # cast to 2d for easier error checking
    matrix = np.atleast_2d(matrix)

    # Check whether matrix is quadratic.
    if np.shape(matrix)[0] != np.shape(matrix)[1]:
        raise ValueError('Matrix is not quadratic: {0}'.format(matrix))

    # check if scalar or tensor higher than 2d
    if matrix.shape[0] == 1 or matrix.ndim > 2:
        raise ValueError('Matrix is not 2d: {0}'.format(matrix))


def format_state_traj(trajs):
    """Convert state trajectory to list of ndarrays.

    Parameters
    ----------
    trajs : list or ndarray or list of ndarray
        State trajectory/trajectories. The states should start from zero and
        need to be integers.

    Returns
    -------
    trajs : list of ndarray
        Return list of ndarrays of integers.

    """
    # list or tuple
    if isinstance(trajs, (tuple, list)):
        # list of integers
        if all((np.issubdtype(type(state), np.integer) for state in trajs)):
            trajs = [np.array(trajs)]
        # list of lists
        elif all((isinstance(traj, list) for traj in trajs)):
            trajs = [np.array(traj) for traj in trajs]
    # ndarray
    if isinstance(trajs, np.ndarray):
        if len(trajs.shape) == 1:
            trajs = [trajs]
        elif len(trajs.shape) == 2:
            trajs = list(trajs)

    # check for integers
    _check_state_traj_type(trajs)

    return trajs


def _check_state_traj_type(trajs):
    """Check if state trajectory is correct formatted."""
    # check for integers
    for traj in trajs:
        if not isinstance(traj, np.ndarray):
            raise TypeError(
                'Trajs need to be np.ndarray but are {0}'.format(type(traj)),
            )
        if not np.issubdtype(traj.dtype, np.integer):
            raise TypeError(
                'States needs to be integers but are {0}'.format(traj.dtype),
            )
    return True


def _flatten_data(array):
    """Flatten data to 1D ndarray.

    This method flattens ndarrays, list of ndarrays to a 1D ndarray. This can
    be undone with _unflatten_data().

    Parameters
    ----------
    array : ndarray, list, list of ndarrays
        1D data or a list of data.

    Returns
    -------
    data : ndarray
        Flattened data.

    kwargs : dict
        Dictionary with information to restore shape.

    """
    kwargs = {}

    # flatten data
    if isinstance(array, list):
        # list of ndarrays
        if all((isinstance(row, np.ndarray) for row in array)):
            # get shape and flatten
            kwargs['limits'] = np.cumsum([len(row) for row in array])
            array = np.concatenate(array)
        # list of numbers
        else:
            array = np.asarray(array)
    elif isinstance(array, np.ndarray):
        # get shape and flatten
        kwargs['data_shape'] = array.shape
        array = array.flatten()

    return array, kwargs


def _unflatten_data(array, kwargs):
    """Unflatten data to original structure.

    This method undoes _flatten_data().

    Parameters
    ----------
    array : ndarray
        Flattened data.

    kwargs : dict
        Dictionary with information to restore shape. Provided by
        _flatten_data().

    Returns
    -------
    array : ndarray, list, list of ndarrays
        Data with restored shape.

    """
    # parse kwargs
    data_shape = kwargs.get('data_shape')
    limits = kwargs.get('limits')

    # reshape
    if data_shape is not None:
        array = array.reshape(data_shape)
    elif limits is not None:
        array = np.split(array, limits)[:-1]

    return array
