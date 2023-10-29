# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath("../"))

from ezbot import __version__

project = "EzBot"
copyright = f"{date.today().year}, tibue99"
author = "tibue99"
release = __version__
version = __version__


# General configuration
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
]

always_document_param_types = True
simplify_optional_unions = True

autodoc_member_order = "bysource"

intersphinx_mapping = {
    "py": ("https://docs.python.org/3", None),
    "dc": ("https://discordpy.readthedocs.io/en/stable/", None),
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# Options for HTML output and furo customisation
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
# https://pradyunsg.me/furo/customisation/

html_theme = "furo"
html_static_path = ["_static"]

html_title = f"<h3 align='center'>{release}</h3>"
html_logo = "_static/ezbot.png"
html_favicon = "_static/favicon.ico"
