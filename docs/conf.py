import os
import sys
import inspect
import shutil
import sphinx_rtd_theme
from sphinx.ext import apidoc
import sphinx

__location__ = os.path.join(os.getcwd(), os.path.dirname(
    inspect.getfile(inspect.currentframe())))
sys.path.insert(0, os.path.join(__location__, '../src'))

#####
# Create API docs
output_dir = os.path.join(__location__, "api")
module_dir = os.path.join(__location__, "../src/jupyter_process_manager")
try:
    shutil.rmtree(output_dir)
except FileNotFoundError:
    pass

try:
    cmd_line_template = "sphinx-apidoc -f -o {outputdir} {moduledir}"
    cmd_line = cmd_line_template.format(outputdir=output_dir, moduledir=module_dir)
    args = cmd_line.split(" ")
    args = args[1:]
    apidoc.main(args)
except Exception as e:
    print("Running `sphinx-apidoc` failed!\n{}".format(e))

#####
# General configuration
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'sphinx.ext.todo',
              'sphinx.ext.autosummary', 'sphinx.ext.viewcode', 'sphinx.ext.coverage',
              'sphinx.ext.doctest', 'sphinx.ext.ifconfig', 'sphinx.ext.mathjax',
              'sphinx.ext.napoleon', "sphinx_rtd_theme"]

napoleon_google_docstring = False
napoleon_numpy_docstring = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
# The suffix of source filenames.
source_suffix = '.rst'
# The master toctree document.
master_doc = 'index'
# General information about the project.
project = u'jupyter_process_manager'
copyright = u'2021, Stanislav Prokopyev'

# The short X.Y version.
version = ''  # Is set by calling `setup.py docs`
# The full version, including alpha/beta/rc tags.
release = ''  # Is set by calling `setup.py docs`
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']
# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False
# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

#####
# Options for HTML output
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
# html_theme_options = {
#     'sidebar_width': '300px',
#     'page_width': '80%'
# }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_last_updated_fmt = '%b %d, %Y'

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True
html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = True

# Output file base name for HTML help builder.
htmlhelp_basename = 'jupyter_process_manager-doc'