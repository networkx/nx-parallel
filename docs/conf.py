# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "nx-parallel"
copyright = "2026, nx-parallel contributors"
author = "Aditi Juneja"
release = "0.4"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_nb",
    "autoapi.extension",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
]
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "myst-nb",
    ".ipynb": "myst-nb",
}

# Use the outputs already stored in the notebook instead of re-executing it
# (it needs dask/ray/free-threaded Python, which the docs CI doesn't have).
nb_execution_mode = "off"

# GitHub-style anchors for h1-h3, so links like [..](#21-usage) work
myst_heading_anchors = 3

templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**.ipynb_checkpoints",
    "timing/index.md",  # timing page not ready yet; remove to publish it
]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_logo = "_static/nx_parallel_banner.svg"
html_static_path = ["_static"]

html_theme_options = {
    "navbar_start": ["navbar-logo"],
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "navbar_persistent": ["search-button"],
    "secondary_sidebar_items": ["page-toc", "edit-this-page"],
    "github_url": "https://github.com/networkx/nx-parallel/",
}

autoapi_type = "python"
autoapi_dirs = ["../nx_parallel", "../_nx_parallel"]
autoapi_root = "api/"
autoapi_keep_files = False
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
]
autoapi_ignore = [
    "*/tests/*",
    "*/test_*.py",
    "*/benchmarks/*",
    "*/timing/*",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "networkx": ("https://networkx.org/documentation/stable/", None),
}
