from __future__ import annotations

import argparse

from libcst import codemod

from bot_formatter.formatters import DPY, EZCORD, PYCORD


class Output:
    modified_files: list[str] = []
    failed_files: list[str] = []

    def __init__(self, config: argparse.Namespace):
        self.config = config

    def success(self, file: str):
        self.modified_files.append(file)

    def error(self, file: str, error: Exception):
        self.failed_files.append(f"{file}: {error}")

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

        self.config = parser.parse_args(args)
        self.report = Output(self.config)

        if not self.config.files:
            parser.print_help()
            return

        for file in self.config.files:
            self.format_file(file)

        self.report.print_output()

    def log(self, message: str):
        """Prints a message to the console if the silent mode isn't enabled."""
        if not self.config.silent:
            print(message)

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

        for formatter in formatters:
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
