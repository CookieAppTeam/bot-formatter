# Configuration
There are several configuration options available.
You can either pass them as command-line arguments or pass them into your `.pre-commit-config.yaml` file.

| Argument             | Description                                                                          |
|----------------------|--------------------------------------------------------------------------------------|
| `--silent`           | Disable all outputs.                                                                 |
| `--dry-run`          | Checks files without changing them.                                                  |
| `--lib {dpy,pycord}` | Whether to use `Discord.py` or `Pycord`. Default to `Pycord`.                        |
| `--ezcord`           | Enables `Ezcord` checks.                                                             |
| `--no-yaml`          | Disables YAML formatters.                                                            |
| `--lang`             | Set the directory for your language files. Files in this directory will be compared. |


These options can also be viewed with the `--help` argument.
