from __future__ import annotations

import argparse

from libcst import codemod

from ezbot.formatters import ENABLED_FORMATTERS


class EzBot:
    def __init__(self, args) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument("filenames", nargs="*")

        self.config = parser.parse_args(args)

        for file in self.config.filenames:
            self.format_file(file)

    def format_file(self, filename: str):
        try:
            with open(filename, encoding="utf-8") as f:
                code = f.read()
        except Exception as e:
            print(f"Could not read file {filename}: {e}")

        for formatter in ENABLED_FORMATTERS:
            transformer = formatter(codemod.CodemodContext(filename=filename))
            result = codemod.transform_module(transformer, code)

            if isinstance(result, codemod.TransformSuccess):
                if result.code != code:
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(result.code)
                        print(f"Formatted {filename}")

            elif isinstance(result, codemod.TransformFailure):
                print(f"Failed to format {filename}: {result.error}")
