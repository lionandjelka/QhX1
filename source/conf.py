# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'QhX'
copyright = '2023, Andjelka Kovacevic'
author = 'Andjelka Kovacevic'
release = '2023'

version = '0.1.1'  # The short X.Y version
release = '0.1.1'  # The full version, including alpha/beta/rc tags

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',  # Include documentation from docstrings
    'sphinx.ext.viewcode',  # Add links to source code
    'sphinx.ext.napoleon',  # Support for NumPy and Google style docstrings
    'sphinx.ext.todo',      # Support for todo items
    'sphinx.ext.coverage',  # Checks documentation coverage
    'sphinx.ext.intersphinx', # Link to other project's documentation
    'sphinx.ext.mathjax',   # Render math via JavaScript
    'sphinx.ext.githubpages',# Publish HTML files to GitHub pages
    'nbsphinx',
]

source_suffix = '.rst'
master_doc = 'index'
import os
import sys
sys.path.insert(0, os.path.abspath('../QhX'))


templates_path = ['_templates']
exclude_patterns = []

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

#html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
#html_theme_options = {
#    'logo_only': False,
#    'display_version': True,
#    'prev_next_buttons_location': 'bottom',
#    'style_external_links': True,
#    'style_nav_header_background': 'white',
    # Toc options
#    'collapse_navigation': False,
#    'sticky_navigation': True,
#    'navigation_depth': 4,
#    'includehidden': True,
#    'titles_only': False
#}

html_theme_options = {
    'analytics_id': 'G-XXXXXXXXXX',  #  Provided by Google in your dashboard
    'analytics_anonymize_ip': False,
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': 'white',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': -1,
    'includehidden': True,
    'titles_only': False
}
html_logo = '_static/logo.png'

html_static_path = ['_static']
