"""
Filename: vdtabulate.py
Version: 0.0.0
Last updated: 2019-04-28
Home: https://github.com/jsvine/visidata-plugins
Author: Jeremy Singer-Vine

# Usage

This plugin makes it possible to save sheets as text-tables, using
the "tabulate" library: https://bitbucket.org/astanin/python-tabulate 

See
https://bitbucket.org/astanin/python-tabulate#rst-header-table-format
for valid table format options.

## Commands

- `tabulate-copy` copies the sheet, as a text-table, to your clipboard
- `tabulate-save` saves the sheet, as a text-table, to file

## Options

- `tabulate_format` specifies the default text-table format

"""

__version__ = "0.0.0"

from tabulate import tabulate

from visidata import (
    Sheet,
    addGlobals,
    copyToClipboard,
    Path,
    asyncthread,
    option,
    options,
    status,
    confirm,
    fail,
    Progress
)

DEFAULT_FORMAT = "simple"

option("tabulate_format", DEFAULT_FORMAT, "Default format for 'tabulate' commands")

SUPPORTED_FORMATS = [
    "plain",
    "simple",
    "github",
    "grid",
    "fancy_grid",
    "pipe",
    "orgtbl",
    "jira",
    "presto",
    "psql",
    "rst",
    "mediawiki",
    "moinmoin",
    "youtrack",
    "html",
    "latex",
    "latex_raw",
    "latex_booktabs",
    "textile",
]

def to_tabulate_table(sheet, fmt):
    if fmt not in SUPPORTED_FORMATS:
        fail(f"'{fmt}' is not a supported 'tabulate' format")

    headers = [ col.name for col in sheet.visibleCols ]

    def get_row_values(row):
        return [ col.getDisplayValue(row) for col in sheet.visibleCols ]

    return tabulate(
        map(get_row_values, Progress(sheet.rows)),
        headers,
        tablefmt = fmt
    )

@asyncthread
def copy_tabulate(sheet, fmt):
    tbl = to_tabulate_table(sheet, fmt)
    copyToClipboard(tbl)

@asyncthread
def _save_table(sheet, fmt, p):
    status(f"saving to {p.fqpn} as '{fmt}' table format")

    tbl = to_tabulate_table(sheet, fmt)

    with p.open_text(mode = "w") as fp:
        fp.write(tbl)

    status(f"{p} save finished")

def save_tabulate(sheet, givenpath, confirm_overwrite = True):
    p = Path(givenpath)

    if p.exists():
        if confirm_overwrite:
            confirm(f"{givenpath} already exists. overwrite? ")

    _save_table(sheet, options.tabulate_format, p)


Sheet.copy_tabulate = copy_tabulate
Sheet.save_tabulate = save_tabulate

Sheet.addCommand(None, "tabulate-copy", "vd.sheet.copy_tabulate(input('copy sheet to clipboard as table format: ', value = options.tabulate_format))")

Sheet.addCommand(None, "tabulate-save", "vd.sheet.save_tabulate(inputFilename('save to: ', value = (sheet.name.strip('.') or 'directory') + '.txt'), confirm_overwrite = options.confirm_overwrite)")

addGlobals({
    "save_tabulate": save_tabulate
})
