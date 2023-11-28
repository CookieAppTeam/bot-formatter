from __future__ import annotations

import argparse

from libcst import codemod

from ezbot.formatters import ENABLED_FORMATTERS


class EzBot:
    def __init__(self, args: list[str]) -> None:
        parser = argparse.ArgumentParser(prog="ezbot")
        parser.add_argument("files", nargs="*", help="The files to format.")
        parser.add_argument("--silent", action="store_true", help="Hide all log messages.")
        parser.add_argument(
            "--dry-run", action="store_true", help="Scan files without modifying them."
        )

        self.config = parser.parse_args(args)

        if not self.config.files:
            parser.print_help()
            return

        self.modified_files = 0

        for file in self.config.files:
            self.format_file(file)

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
            self.log(f"Could not read file {filename}: {e}\n")
            return

        for formatter in ENABLED_FORMATTERS:
            transformer = formatter(codemod.CodemodContext(filename=filename))
            result = codemod.transform_module(transformer, code)

            if isinstance(result, codemod.TransformSuccess):
                if result.code != code:
                    if self.config.dry_run:
                        self.log(f"Would format {filename}\n")
                    else:
                        with open(filename, "w", encoding="utf-8") as f:
                            f.write(result.code)
                            self.log(f"Formatted {filename}\n")
                            self.modified_files += 1

            elif isinstance(result, codemod.TransformFailure):
                self.log(f"Failed to format {filename}: {result.error}\n")

        self.log(f"\nModified {self.modified_files} files (checked {len(self.config.files)} files)")
