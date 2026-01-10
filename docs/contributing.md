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
