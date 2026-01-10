from __future__ import annotations

import argparse
from pathlib import Path

from libcst import codemod
import yaml

from bot_formatter.formatters import DPY, EZCORD, PYCORD, LANG


class Output:
    modified_files: list[str] = []
    failed_files: list[str] = []
    failed_checks: dict[str, list[str]] = {}

    def __init__(self, config: argparse.Namespace):
        self.config = config

    def success(self, file: str):
        self.modified_files.append(file)

    def error(self, file: str, error: Exception):
        self.failed_files.append(f"{file}: {error}")

    def check_failed(self, file: str, error_txt: str):
        self.failed_checks[file] = error_txt

    @staticmethod
    def _check_plural(word: str, count: int) -> str:
        return f"{count} {word}{'s' if count != 1 else ''}"

    def print_output(self):
        """Prints a report to the console if the silent mode isn't enabled."""

        if self.config.silent:
            return

        modify = self._check_plural("file", len(self.modified_files))
        check = self._check_plural("file", len(self.config.files))

        if self.config.dry_run:
            report = f"Done! Would modify {modify} (checked {check})"
        else:
            report = f"Done! Modified {modify} (checked {check})"

        if self.modified_files:
            report += "\n\n" + "\n".join(self.modified_files)

        if self.failed_files:
            report += f"\n\n{self._check_plural('error', len(self.failed_files))} occurred"
            report += "\n" + "\n".join(self.failed_files)

        for file, errors in self.failed_checks.items():
            report += f"\n\n\n------ CHECKS FAILED IN {file.upper()} ------"
            report += "\n\n" + "\n".join(errors)

        print(report)


class BotFormatter:
    def __init__(self, args: list[str]) -> None:
        parser = argparse.ArgumentParser(prog="bot-formatter")
        parser.add_argument("files", nargs="*", help="The files to format.")
        parser.add_argument("--silent", action="store_true", help="Hide all log messages.")
        parser.add_argument(
            "--dry-run", action="store_true", help="Scan files without modifying them."
        )
        parser.add_argument(
            "--lib", default="pycord", choices=["dpy", "pycord"], help="The library to use."
        )
        parser.add_argument("--ezcord", action="store_true", help="Use Ezcord formatters.")
        parser.add_argument("--no-yaml", action="store_true", help="Disable YAML formatters.")
        parser.add_argument("--lang", help="The language directory to check.")

        self.config = parser.parse_args(args)
        self.report = Output(self.config)

        if not self.config.files:
            parser.print_help()
            return

        if self.config.lang:
            self.lang_dir = Path(self.config.lang)
            if not self.lang_dir.is_dir():
                raise ValueError(f"The language directory '{self.lang_dir}' is not a valid directory.")
        else:
            self.lang_dir = None

        self.check_lang_files()

        for file in self.config.files:
            self.format_file(file)

        self.report.print_output()

        if len(self.report.failed_checks) > 0:
            raise SystemExit(1)

    def log(self, message: str):
        """Prints a message to the console if the silent mode isn't enabled."""

        if not self.config.silent:
            print(message)

    def check_lang_files(self):
        """Run language file checks to ensure consistency across all language files."""

        if not self.lang_dir:
            return

        lang_files = list(self.lang_dir.glob("*.yaml")) + list(self.lang_dir.glob("*.yml"))

        lang_contents = {}
        for file_path in lang_files:
            with open(file_path, encoding="utf-8") as f:
                content = yaml.safe_load(f)
                lang_contents[file_path.name] = content

        def collect_keys(lang_content: dict, parent_key: str | None = None) -> set[str]:
            """Recursively collects all keys in a nested dictionary."""

            lang_keys = set()
            for key, value in lang_content.items():
                full_key = f"{parent_key}.{key}" if parent_key else key
                lang_keys.add(full_key)
                if isinstance(value, dict):
                    lang_keys.update(collect_keys(value, full_key))

            return lang_keys

        # detect differences in lang_contents
        for file_name, content in lang_contents.items():
            errors = []
            for other_file_name, other_content in lang_contents.items():
                if file_name == other_file_name:
                    continue

                keys = collect_keys(content)
                other_keys = collect_keys(other_content)

                missing_keys = other_keys - keys

                if missing_keys:
                    missing = '\n'.join(sorted([f"- {key}" for key in missing_keys]))
                    errors.append(f"Missing keys compared to {other_file_name}:\n{missing}")

            if errors:
                self.report.check_failed(file_name, errors)


    def format_file(self, filename: str):
        """Runs all enabled formatters on a given file."""
        try:
            with open(filename, encoding="utf-8") as f:
                code = f.read()
        except Exception as e:
            self.report.error(filename, e)
            return

        formatters = []
        if self.config.lib == "pycord":
            formatters.extend(PYCORD)
        elif self.config.lib == "dpy":
            formatters.extend(DPY)
        if self.config.ezcord:
            formatters.extend(EZCORD)

        ext = filename.split(".")[-1]

        for formatter in formatters:
            if ext != "py":
                continue

            transformer = formatter(codemod.CodemodContext(filename=filename))
            result = codemod.transform_module(transformer, code)

            if isinstance(result, codemod.TransformSuccess):
                if result.code != code:
                    self.report.success(filename)

                    if not self.config.dry_run:
                        with open(filename, "w", encoding="utf-8") as f:
                            f.write(result.code)

            elif isinstance(result, codemod.TransformFailure):
                self.report.error(filename, result.error)

        # Run language formatters
        if self.config.no_yaml or ext not in ["yaml", "yml"]:
            return

        for lang_formatter in LANG:
            new_code = lang_formatter(code)

            if new_code != code:
                self.report.success(filename)
                if not self.config.dry_run:
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(new_code)
