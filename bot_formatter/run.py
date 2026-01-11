from __future__ import annotations

import argparse
from pathlib import Path
from typing import get_type_hints

import yaml
from libcst import codemod

from bot_formatter.formatters import DPY, EZCORD, LANG, PYCORD, YML


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
        if file not in self.failed_checks:
            self.failed_checks[file] = []
        self.failed_checks[file].append(error_txt)

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
            report += "\n\n" + "\n\n".join(errors)

        print(report)


class BotFormatter:
    def __init__(self, args: list[str]) -> None:
        parser = argparse.ArgumentParser(prog="bot-formatter")
        parser.add_argument(
            "files",
            nargs="*",
            help="The files to format. When using pre-commit, this is provided automatically.",
        )
        parser.add_argument(
            "--all", "-a", action="store_true", help="Format all files in the current directory."
        )
        parser.add_argument(
            "--lang-dir",
            type=Path,
            help="The language directory to check. YAML files in this directory will be compared.",
        )

        logs = parser.add_mutually_exclusive_group()
        logs.add_argument("--silent", "-s", action="store_true", help="Hide all log messages.")
        logs.add_argument(
            "--verbose", "-v", action="store_true", help="Show detailed log messages."
        )
        parser.add_argument(
            "--dry-run", action="store_true", help="Scan files without modifying them."
        )

        formatters = parser.add_argument_group("formatters")
        formatters.add_argument(
            "--lib",
            default="none",
            choices=["dpy", "pycord", "none"],
            help="Enable formatters for a Discord library. Defaults to 'none'.",
        )
        formatters.add_argument("--ezcord", action="store_true", help="Enable Ezcord formatters.")
        formatters.add_argument(
            "--yaml",
            action=argparse.BooleanOptionalAction,
            default=True,
            help="Enable YAML formatters.",
        )

        self.config = parser.parse_args(args)
        self.report = Output(self.config)

        if not self.config.files and not self.config.all and not self.config.lang_dir:
            parser.print_help()
            return

        if self.config.all:
            self.config.files = [
                str(p)
                for p in Path(".").rglob("*")
                if p.is_file()
                and p.suffix in [".py", ".yaml", ".yml"]
                and not any(part.startswith(".") for part in p.parts)
            ]

        # Format each file
        for file in self.config.files:
            self.format_file(file)

        # Check language files
        if self.config.lang_dir:
            if not self.config.lang_dir.is_dir():
                parser.error(f"'{self.config.lang_dir}' is not a valid directory.")
            self.check_lang_files()

        # Print report and exit with error code if needed
        self.report.print_output()
        if len(self.report.failed_checks) > 0:
            raise SystemExit(1)

    def log(self, message: str):
        """Prints a message to the console if verbose mode is enabled."""

        if self.config.verbose:
            print(message)

    def check_lang_files(self):
        """Ensure consistency across all language files."""

        lang_files = list(self.config.lang_dir.glob("*.yaml")) + list(
            self.config.lang_dir.glob("*.yml")
        )
        self.log(f"Checking {len(lang_files)} language files in '{self.config.lang_dir}'")

        # All keys as a dictionary
        lang_keys = {}
        for file_path in lang_files:
            with open(file_path, encoding="utf-8") as f:
                content = yaml.safe_load(f)
                lang_keys[file_path.name] = content

        # All contents as a string
        lang_contents = {}
        for file_path in lang_files:
            with open(file_path, encoding="utf-8") as f:
                code = f.read()
                lang_contents[file_path.name] = code

        for formatter in LANG:
            params = get_type_hints(formatter)

            if "lang_keys" in params and "lang_content" in params:
                formatter(lang_keys, lang_contents, self.report)
            elif "lang_content" in params:
                formatter(lang_contents, self.report)
            elif "lang_keys" in params:
                formatter(lang_keys, self.report)
            else:
                raise ValueError(
                    "Formatter must accept either 'lang_keys' or 'lang_contents' parameter."
                )

    def format_file(self, filename: str):
        """Runs all enabled formatters on a given file."""

        self.log(f"Formatting {filename}")
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

        # Run Python formatters
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

        # Run YAML formatters
        if not self.config.yaml or ext not in ["yaml", "yml"]:
            return

        for lang_formatter in YML:
            new_code = lang_formatter(code)

            if new_code != code:
                self.report.success(filename)
                if not self.config.dry_run:
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(new_code)
