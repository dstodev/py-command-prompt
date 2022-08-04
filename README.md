# How to Run

This project requires:

- [Python 3](https://www.python.org/downloads/)

This project packages with setuptools:

- [Quickstart guide](https://setuptools.pypa.io/en/latest/userguide/quickstart.html)
- [pyproject.toml guide](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html)

## Summary

Assuming `python` aliases to `python3` when necessary. Run from project root:

- `python -m pip install --upgrade setuptools build` to update `setuptools` dependencies
- `python -m pip install -e .` to register the package for development & running the tests
- `python -m unittest discover -s src` to run tests
- `python -m build` to build the distribution packages
