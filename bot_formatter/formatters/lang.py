"""Formatter for YAML language files.

These formatters do not check individual code files, but rather
ensure consistency across all language files in the project.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot_formatter.run import Output


# A dictionary with a mapping of file names to their content
LANG_CONTENT = dict[str, dict]


def _collect_keys(lang_content: dict, parent_key: str | None = None) -> set[str]:
    """Recursively collects all keys in a nested dictionary."""

    lang_keys = set()
    for key, value in lang_content.items():
        full_key = f"{parent_key}.{key}" if parent_key else key
        lang_keys.add(full_key)
        if isinstance(value, dict):
            lang_keys.update(_collect_keys(value, full_key))

    return lang_keys


def check_missing_keys(lang_contents: LANG_CONTENT, report: "Output"):
    """Checks that all language files have the same keys."""

    for file_name, content in lang_contents.items():
        errors = []
        for other_file_name, other_content in lang_contents.items():
            if file_name == other_file_name:
                continue

            keys = _collect_keys(content)
            other_keys = _collect_keys(other_content)

            missing_keys = other_keys - keys

            if missing_keys:
                missing = '\n'.join(sorted([f"- {key}" for key in missing_keys]))
                errors.append(f"Missing keys compared to {other_file_name}:\n{missing}")

        if errors:
            report.check_failed(file_name, errors)
