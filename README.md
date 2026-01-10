# bot-formatter
[![](https://img.shields.io/pypi/v/bot-formatter.svg?style=for-the-badge&logo=pypi&color=yellow&logoColor=white)](https://pypi.org/project/bot-formatter/)
[![](https://img.shields.io/readthedocs/bot-formatter?style=for-the-badge&color=blue&link=https%3A%2F%2Fbot-formatter.readthedocs.io%2F)](https://bot-formatter.readthedocs.io/)
[![](https://img.shields.io/pypi/l/bot-formatter?style=for-the-badge)](https://pypi.org/project/bot-formatter/)
[![](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&style=for-the-badge)](https://github.com/pre-commit/pre-commit)

A formatter and language file validator for Discord bots.
Made for [Ezcord](https://github.com/tibue99/ezcord) language files.

## Installing
Python 3.10 or higher is required.
```
pip install bot-formatter
```

## Usage
To format a file, run:
```
bot-formatter main.py
```
To format YAML language files in a directory, run:
```
bot-formatter --lang path/to/language/dir
```

To view all available options, run
```
bot-formatter --help
```

For a full overview, see the [documentation](https://bot-formatter.readthedocs.io/).

## Pre-Commit
To use `bot-formatter` as a pre-commit hook, add the following to your `.pre-commit-config.yaml`:
```yaml
- repo: https://github.com/CookieAppTeam/bot-formatter
  rev: 0.1.0
  hooks:
    - id: bot-formatter
```

## Local Development
To set up a development environment, clone the repository and install the dependencies:
```
pip install dev-requirements.txt
```
You can then run the formatter for a file of your choice:
```
bot_formatter your_file.py
```
To test the pre-commit hook locally, first get your last commit hash:
```
git rev-parse HEAD
```
Then, add the following to the `.pre-commit-config.yaml` of your project:
```yaml
- repo: ../bot-formatter  # path to your local bot-formatter
  rev: 19295427421e82c67a6423c9e13dd254a2b7bb53  # replace with your last commit hash
  hooks:
    - id: bot-formatter
```
