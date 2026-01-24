"""Formatters for YAML language files that compare content and keys across multiple files."""

import re

# A dictionary with a mapping of file names to their keys
LANG_KEYS = dict[str, dict]

# A dictionary with a mapping of file names to their content
LANG_CONTENT = dict[str, str]


VAR_REGEX = re.compile(r"\{([^}]+)}")


def _collect_keys(dict_content: dict, parent_key: str | None = None) -> set[str]:
    """Recursively collects all keys in a nested dictionary."""

    keys = set()
    for key, value in dict_content.items():
        full_key = f"{parent_key}.{key}" if parent_key else key
        keys.add(full_key)
        if isinstance(value, dict):
            keys.update(_collect_keys(value, full_key))

    return keys


def _collect_keys_ordered(dict_content: dict, parent_key: str | None = None) -> list[str]:
    """Recursively collects all keys in a nested dictionary in order."""

    keys = []
    for key, value in dict_content.items():
        full_key = f"{parent_key}.{key}" if parent_key else key
        keys.append(full_key)
        if isinstance(value, dict):
            keys.extend(_collect_keys_ordered(value, full_key))

    return keys


def _collect_vars(dict_content: dict, parent_key: str | None = None) -> dict[str, set[str]]:
    """Recursively collects all variables per key in a nested dictionary."""

    result = {}
    for key, value in dict_content.items():
        full_key = f"{parent_key}.{key}" if parent_key else key

        if isinstance(value, dict):
            result.update(_collect_vars(value, full_key))
        elif isinstance(value, str):
            vars_found = set(VAR_REGEX.findall(value))
            result[full_key] = vars_found

    return result


def check_missing_keys(lang_keys: LANG_KEYS, report):
    """Checks that all language files have the same keys."""

    for file_name, content in lang_keys.items():
        for other_file_name, other_content in lang_keys.items():
            if file_name == other_file_name:
                continue

            keys = _collect_keys(content)
            other_keys = _collect_keys(other_content)

            missing_keys = other_keys - keys

            if missing_keys:
                missing = "\n".join(sorted([f"- {key}" for key in missing_keys]))
                report.check_failed(
                    file_name, f"Missing keys compared to {other_file_name}:\n{missing}"
                )


def check_key_order(lang_keys: LANG_KEYS, report):
    """Checks that all language files use the same key order and reports keys out of order."""

    reference_file = list(lang_keys)[0]
    reference_order = _collect_keys_ordered(lang_keys[reference_file])

    for file_name, content in lang_keys.items():
        if file_name == reference_file:
            continue

        current_order = _collect_keys_ordered(content)
        wrong_keys = [k for k, ref_k in zip(current_order, reference_order) if k != ref_k]

        if wrong_keys:
            report.check_failed(
                file_name,
                f"Keys in wrong order:\n" + "\n".join(f"- {k}" for k in wrong_keys),
            )


def check_variables(lang_keys: LANG_KEYS, report):
    """Prevents multiple keys with the same prefix in a language file block."""

    collected = {lang: _collect_vars(content) for lang, content in lang_keys.items()}
    files = list(collected.keys())

    base = files[0]
    base_keys = set(collected[base].keys())

    for file_name in files[1:]:
        other_keys = set(collected[file_name].keys())

        for key in base_keys & other_keys:
            base_vars = collected[base][key]
            other_vars = collected[file_name][key]

            if base_vars != other_vars:
                base_diff = base_vars - other_vars
                other_diff = other_vars - base_vars

                report.check_failed(
                    file_name,
                    f"Variable mismatch at '{key}'"
                    f"\n- {base}: {base_diff}"
                    f"\n- {file_name}: {other_diff}",
                )


def check_empty_line_diffs(lang_content: LANG_CONTENT, report):
    """Checks if all YAML keys are in the same line across different language files."""

    reference_file = list(lang_content)[0]
    reference_lines = lang_content[reference_file].splitlines()

    # Compare all files to reference file
    for file_name, content in lang_content.items():
        if file_name == reference_file:
            continue

        current_lines = content.splitlines()

        for line, (ref_line, cur_line) in enumerate(zip(reference_lines, current_lines), start=1):
            if ref_line.strip() == "" and ref_line.strip() != cur_line.strip():
                report.check_failed(file_name, f"Empty line {line} differs from {reference_file}.")
                break
