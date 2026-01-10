# bot-formatter
[![](https://img.shields.io/pypi/v/bot-formatter.svg?style=for-the-badge&logo=pypi&color=yellow&logoColor=white)](https://pypi.org/project/bot-formatter/)
[![](https://img.shields.io/readthedocs/bot-formatter?style=for-the-badge&color=blue&link=https%3A%2F%2Fbot-formatter.readthedocs.io%2F)](https://bot-formatter.readthedocs.io/)
[![](https://img.shields.io/pypi/l/bot-formatter?style=for-the-badge)](https://pypi.org/project/bot-formatter/)

A formatter for Discord bots.

## Installing
Python 3.10 or higher is required.
```
pip install bot-formatter
```

## Usage
For a full overview, see the [documentation](https://bot-formatter.readthedocs.io/).
```
bot-formatter main.py
```

## Pre-Commit
```yaml
- repo: https://github.com/CookieAppTeam/bot-formatter
  rev: 0.1.0
  hooks:
    - id: bot-formatter
```
