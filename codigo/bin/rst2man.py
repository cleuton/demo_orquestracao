#!/home/cleuton/Documents/projetos/eda_curso/02-Padrões utilizados em EDA/02-02-orquestração/codigo/bin/python3

# Author:
# Contact: grubert@users.sf.net
# Copyright: This module has been placed in the public domain.

"""
man.py
======

This module provides a simple command line interface that uses the
man page writer to output from ReStructuredText source.
"""

import locale
try:
    locale.setlocale(locale.LC_ALL, '')
except Exception:
    pass

from docutils.core import publish_cmdline, default_description
from docutils.writers import manpage

description = ("Generates plain unix manual documents.  "
               + default_description)

publish_cmdline(writer=manpage.Writer(), description=description)
