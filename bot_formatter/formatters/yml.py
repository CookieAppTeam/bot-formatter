"""Formatter for YAML files."""


def remove_duplicate_new_lines(content: str) -> str:
    """Removes duplicate new lines from the content of a YAML file."""

    while "\n\n\n" in content:
        content = content.replace("\n\n\n", "\n\n")

    return content
