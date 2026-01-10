# Getting Started
![](assets/logo.png)

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

For a full overview, see the [config](config.md) page.

## Pre-Commit
To use `bot-formatter` as a pre-commit hook, add the following to your `.pre-commit-config.yaml`:
```yaml
- repo: https://github.com/CookieAppTeam/bot-formatter
  rev: 0.1.0
  hooks:
    - id: bot-formatter
```
