import argparse
import unittest

from bot_formatter.formatters.lang import _build_key_line_map, check_missing_keys
from bot_formatter.formatters.yml import remove_duplicate_new_lines
from bot_formatter.run import Output


class FormatterTests(unittest.TestCase):
    def test_yaml_formatter_removes_repeated_blank_lines(self):
        self.assertEqual(
            remove_duplicate_new_lines("key: value\n\n\nnext: value\n"),
            "key: value\n\nnext: value\n",
        )

    def test_key_line_map_tracks_nested_keys_and_skips_comments(self):
        content = "# ignored: comment\nmenu:\n  options:\n    first: One\n"

        self.assertEqual(
            _build_key_line_map(content),
            {"menu": 2, "menu.options": 3, "menu.options.first": 4},
        )

    def test_missing_keys_are_reported_for_the_language_that_lacks_them(self):
        class Report:
            def __init__(self):
                self.failures = []

            def check_failed(self, file_name, message):
                self.failures.append((file_name, message))

        report = Report()
        keys = {"en.yaml": {"greeting": "Hello"}, "de.yaml": {}}
        content = {"en.yaml": "greeting: Hello\n", "de.yaml": ""}

        check_missing_keys(keys, content, report)

        self.assertEqual(len(report.failures), 1)
        self.assertEqual(report.failures[0][0], "de.yaml")
        self.assertIn("greeting", report.failures[0][1])

    def test_output_state_is_independent_per_instance(self):
        first = Output(argparse.Namespace())
        second = Output(argparse.Namespace())

        first.success("one.py")

        self.assertEqual(first.modified_files, ["one.py"])
        self.assertEqual(second.modified_files, [])


if __name__ == "__main__":
    unittest.main()
