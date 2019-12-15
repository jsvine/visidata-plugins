"""
Filename: vddedupe.py
Version: 0.0.1
Last updated: 2019-01-01
Home: https://github.com/jsvine/visidata-plugins
Author: Jeremy Singer-Vine

# Usage

Duplicates are determined by the sheet's key columns.

If no key columns are specified, then a duplicate row is one where the values
of *all non-hidden* columns are exactly the same as a row that occurs earlier
in the sheet.

If key columns *are* specified, then duplicates are detected based on the
values in just those columns.

## Commands

- `select-duplicate-rows` sets the selection status in VisiData to `selected`
  for each row in the active sheet that is a duplicate of a prior row.

- `dedupe-rows` pushes a new sheet in which only non-duplicate rows in the
  active sheet are included.
"""

from visidata import (
    Sheet,
    asyncthread,
    copy,
    warning,
    Progress,
    vd
)

def gen_identify_duplicates(sheet):
    """
    Takes a sheet, and returns a generator yielding a tuple for each row
    encountered. The tuple's structure is `(row_object, is_dupe)`, where
    is_dupe is True/False.

    See note in Usage section above regarding how duplicates are determined.
    """

    keyCols = sheet.keyCols

    cols_to_check = None
    if len(keyCols) == 0:
        warning("No key cols specified. Using all columns.")
        cols_to_check = sheet.visibleCols
    else:
        cols_to_check = sheet.keyCols

    seen = set()
    for r in Progress(sheet.rows):
        vals = tuple(col.getValue(r) for col in cols_to_check)
        is_dupe = vals in seen
        if not is_dupe:
            seen.add(vals)
        yield (r, is_dupe)


@asyncthread
def select_duplicate_rows(sheet, duplicates = True):
    """
    Given a sheet, sets the selection status in VisiData to `selected` for each
    row that is a duplicate of a prior row.

    If `duplicates = False`, then the behavior is reversed; sets the selection
    status to `selected` for each row that is *not* a duplicate.
    """
    before = len(sheet.selectedRows)

    for row, is_dupe in gen_identify_duplicates(sheet):
        if is_dupe == duplicates:
            sheet.selectRow(row)

    sel_count = len(sheet.selectedRows) - before

    more_str = " more" if before > 0 else ""

    vd.status("selected {}{} {}".format(
        sel_count,
        more_str,
        sheet.rowtype
    ))

@asyncthread
def dedupe_rows(sheet):
    """
    Given a sheet, pushes a new sheet in which only non-duplicate rows are
    included.
    """
    vs = copy(sheet)
    vs.name += "_deduped"
    vd.rows = [row for row, is_dupe in gen_identify_duplicates(sheet) if not is_dupe]
    vd.push(vs)

# Set the two main functions above as methods on the Sheet class
Sheet.select_duplicate_rows = select_duplicate_rows
Sheet.dedupe_rows = dedupe_rows

# Add longname-commands to VisiData to execute these methods
Sheet.addCommand(None, "select-duplicate-rows", "vd.sheet.select_duplicate_rows()")
Sheet.addCommand(None, "dedupe-rows", "vd.sheet.dedupe_rows()")

"""
# Changelog

## 0.0.1 - 2019-01-01

Internal change, no external effects: Migrates from ._selectedRows to .selectedRows.

## 0.0.0 - 2018-12-30

Initial release.
"""
