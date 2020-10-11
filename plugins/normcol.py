"""
Filename: vdnormcol.py
Version: 0.0.0
Last updated: 2018-12-31
Home: https://github.com/jsvine/visidata-plugins
Author: Jeremy Singer-Vine

# Usage

This plugin normalizes column names in any given sheet, so that the names are:

- Composed only of lowercase letters, numbers, and underscores.

- Valid Python identifiers. This is mostly handled by the rule above, but also
  prohibits names beginning with a digit; that is handled by prefixing those
  names with an underscore.

- Unique within the sheet. Non-unique names are suffixed with "__" and an
  integer.

Unnamed columns are left as such.

For instance, a sheet with the following columns names:

- "Genus, Species"
- "Height"
- "5-score"
- "Height"
- ""
- ""

... would be converted to have the following column names:

- "genus_species"
- "height__0"
- "_5_score"
- "height__1"
- ""
- ""

## Commands

- `normalize-col-names` normalizes the names of all *non-hidden* columns in the
  active sheet, per the approach described above. Alias:
      `normalize-column-names`.

"""

from visidata import Sheet
from collections import Counter
import re

nonalphanum_pat = re.compile(r"[^a-z0-9]+")
DIGITS = "0123456789"

def normalize_name(name):
    """
    Given a string, return a normalized string, per the first two rules
    described above.
    """
    # Lowercase and replace all non-alphanumeric characters with _
    subbed = re.sub(nonalphanum_pat, "_", name.lower())

    # Remove leading and trailing _s
    stripped = subbed.strip("_")

    # To ensure it's a valid Python identifier
    if (stripped or "_")[0] in DIGITS:
        stripped = "_" + stripped

    return stripped

def gen_normalize_names(names):
    """
    Given a list of strings, yield fully-normalized conversions of those
    strings, ensuring that each is unique.
    """
    base = list(map(normalize_name, names))
    counts = Counter(base)
    
    # Append __{i} to non-unique names
    seen = dict((key, 0) for key in counts.keys())
    for name in base:
        if counts[name] == 1 or name == "":
            norm_name = name
        else:
            norm_name = name + "__" + str(seen[name])
            seen[name] += 1
        yield norm_name

def normalize_names(names):
    return list(gen_normalize_names(names))

def normalize_column_names(sheet):
    """
    Normalize the names of all non-hidden columns on the active sheet.
    """
    new_names = normalize_names(c.name for c in sheet.visibleCols)
    for i, c in enumerate(sheet.visibleCols):
        c.name = new_names[i]

# Set the function above as methods on the Sheet class
Sheet.normalize_column_names = normalize_column_names

# Add longname-commands to VisiData to execute these methods
cmd_str = "vd.sheet.normalize_column_names()"
Sheet.addCommand(None, "normalize-col-names", cmd_str)
Sheet.addCommand(None, "normalize-column-names", cmd_str)
