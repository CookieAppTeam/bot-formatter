# Configuration
There are several configuration options available. You can either pass them as
command-line arguments or write them into your `.pre-commit-config.yaml` file.

!!! tip
    These options can also be viewed with the `--help` argument.

## Positional Arguments
| Argument | Description                                                                           |
|----------|---------------------------------------------------------------------------------------|
| `files`  | One or more files to format. When using `pre-commit`, this is provided automatically. |

## Options
| Argument     | Description                                                                       |
|--------------|-----------------------------------------------------------------------------------|
| `--lang-dir` | The language directory to check. YAML files in this directory will be compared.   |
| `--silent`   | Disable all outputs.                                                              |
| `--dry-run`  | Check files without modifying them.                                               |

## Formatters
| Argument                  | Description                                                         |
|---------------------------|---------------------------------------------------------------------|
| `--lib {dpy,pycord,none}` | Enable formatters for `Discord.py` or `Pycord`. Defaults to `none`. |
| `--ezcord`                | Enable `Ezcord` formatters. Disabled by default.                    |
| `--yaml` `--no-yaml`      | Enable or disable YAML formatters. Enabled by default.              |

For usage examples, see the [Getting Started](index.md#usage) page.
