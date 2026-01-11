# ✏️ Formatters
This library includes several formatters and checks for Python and YAML files.

!!! tip
    To enable and disable specific formatters, see the [Configuration](config.md) page.


| Symbol | Description                                                |
|--------|------------------------------------------------------------|
| 🛠️    | This formatter modifies the file.                          |
| 🔍     | This check only reports issues without modifying the file. |


## YAML
Formatters for YAML files.

| Type | Name                         | Description                                |
|------|------------------------------|--------------------------------------------|
| 🛠️  | `remove_duplicate_new_lines` | Removes duplicate new lines in YAML files. |

## YAML Language Files
These checks compare **all language files** in the specified language directory when using
the `--lang-dir` option.

| Type | Name                     | Description                                                                       |
|------|--------------------------|-----------------------------------------------------------------------------------|
| 🔍   | `check_missing_keys`     | Reports missing keys between language files.                                      |
| 🔍   | `check_empty_line_diffs` | Checks that sections are consistent between language files comparing empty lines. |

## Ezcord
Formatters for [Ezcord](https://github.com/tibue99/ezcord) when using the ``--ezcord`` option.

| Type | Name             | Description                                                    |
|------|------------------|----------------------------------------------------------------|
| 🛠️  | `ConvertContext` | Replaces `discord.ApplicationContext` with `ezcord.EzContext`. |

## Discord.py
Formatters for `discord.py` when using the `--lib dpy` option.

| Type | Name           | Description                            |
|------|----------------|----------------------------------------|
| 🛠️  | `ConvertSetup` | Make cog setup functions asynchronous. |
