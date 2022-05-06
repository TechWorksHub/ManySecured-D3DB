# Contributing to ManySecured-D3DB

This is a project that is hosted on GitHub. To contribute, you can fork the project and make your own changes.

## Writing Code

We recommend using [pre-commit](https://pre-commit.com/) to check your contributions before they are committed.

Pre-commit may be installed via your OS's package manager, however we recommend installing via `pip` to
get the latest version (requires Python3 and Pip):

```bash
pip3 install pre-commit
```

Then, you can setup pre-commit in this project using:

```bash
pre-commit install
```

This will automatically run some formatting/linting checks before making a `git commit`.
You can also manually run `pre-commit` on all files by doing `pre-commit run --all-files`.
