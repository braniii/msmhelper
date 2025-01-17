# Welcome to the `msmhelper` Maintenance Guideline

This guide will give you an overview of how to publish a new version of msmhelper. In the following we will refer to the new version as `v1.*.*`. This needs to be substituted to the current version, e.g. `v1.1.3`.

## Prepare New Release
Please ensure that,
1. the version number in `setup.py` and `src/msmhelper/__init__.py` are bumped,
1. a new tag is created via `git tag v1.*.*` and pushed `git push --tags`, and 
1. the changelog includes the new tag and all changes of the release.
As an example see for e.g. the commit of `v1.0.2`, [`132673a`](https://github.com/moldyn/msmhelper/commit/132673ab172ef8cad83a54ad58fde17d4adf22c3).

## Build and Upload to PyPI

For an introduction, please take a look at the [PyPI manual](https://packaging.python.org/en/latest/tutorials/packaging-projects/).

First ensure that all needed dependencies are installed
```bash
python -m pip install --upgrade pip
python -m pip install --upgrade build
python -m pip install --upgrade twine
```

To create the build, please ensure first that the directory `dist` does not exist. Otherwise delete it,
```bash
rm dist
```
Then, execute
```bash
python3 -m build
``` 
which will create the directory `dist` including the source distributions:
```bash
dist/
├── msmhelper-1.*.*-py3-none-any.whl
└── msmhelper-1.*.*.tar.gz
```
To upload the new files, run
```bash
python3 -m twine upload dist/*
```

## Update on Conda-Forge
Once a new version is published on PyPI, the conda-forge bot will automatically create a pull request on [msmhelper-feedstock](https://github.com/conda-forge/msmhelper-feedstock).

