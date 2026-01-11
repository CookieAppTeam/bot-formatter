# 🤝 Contributing

## Local Development
To set up a development environment, clone the [repository](https://github.com/CookieAppTeam/bot-formatter)
and install the dependencies:
```
pip install dev-requirements.txt
```
You can then run the formatter for a file of your choice:
```
bot_formatter your_file.py
```

## Test Pre-Commit Hook
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

## Documentation
To build the documentation locally, run:
```
mkdocs serve --livereload
```

## Add New Formatters
To add a new formatter, follow these steps:

1. Go to `bot_formatter/formatters/` and locate the appropriate file for your formatter type.
2. Depending on the type, create a new class or function for your formatter.
3. Import and register your formatter in `bot_formatter/formatters/__init__.py`.
4. Update the documentation in `docs/formatters.md` to include your new formatter.

### Parameters

Language file formatters receive the following parameters:

- `lang_keys` - Dictionary with a mapping of file names to their keys.
- `lang_content` - Dictionary with a mapping of file names to their string content.
- `report` - `Output` class used to report issues.

YAML formatters receive the following parameters:

- `content` - String content of the YAML file.
