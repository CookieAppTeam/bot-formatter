[![Bot Formatter](docs/assets/logo.png)](https://github.com/CookieAppTeam/bot-formatter)

[![](https://img.shields.io/pypi/v/bot-formatter.svg?style=for-the-badge&logo=pypi&color=yellow&logoColor=white)](https://pypi.org/project/bot-formatter/)
[![](https://img.shields.io/readthedocs/bot-formatter?style=for-the-badge&color=blue&link=https%3A%2F%2Fbot-formatter.readthedocs.io%2F)](https://bot-formatter.readthedocs.io/)
[![](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&style=for-the-badge)](https://github.com/pre-commit/pre-commit)

A formatter and language file validator for Python Discord bots.

- ✏️ Includes formatters for `Pycord` and `discord.py`.
- 📚 Format and compare YAML files.
- 📝 Supports [Ezcord](https://github.com/tibue99/ezcord) language files.

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
To view all available options, run:
```
bot-formatter --help
```

For a full overview, see the [documentation](https://bot-formatter.readthedocs.io/).

## Pre-Commit
To use `bot-formatter` as a pre-commit hook, add the following lines to your `.pre-commit-config.yaml`:
```yaml
- repo: https://github.com/CookieAppTeam/bot-formatter
  rev: 0.1.1
  hooks:
    - id: bot-formatter
```
