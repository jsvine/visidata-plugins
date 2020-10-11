# Custom VisiData Plugins

This repository serves as a place for me to share VisiData plugins I've written.

All code is released under the MIT License.

## Table of Contents

- [dedupe](dedupe), for deduplicating rows (VisiData v2.x)
- [normcol](#normcol), for normalizing column names (VisiData v1.5.2)
- [tabulate](#tabulate), for copying/saving sheets as text-tables (VisiData v1.5.2, no longer needed for v2.x)
- [fec](#fec), for loading `.fec` files (VisiData v1.5.2)

---

## `dedupe`

This plugin adds two sheet commands to VisiData:

- `select-duplicate-rows` sets the selection status in VisiData to `selected` for each row in the active sheet that is a duplicate of a prior row.

- `dedupe-rows` pushes a new sheet in which only non-duplicate rows in the active sheet are included.

See [the plugin file](plugins/dedupe) for usage details.

## `normcol`

This plugin normalizes column names in any given sheet, so that the names are:

- Composed only of lowercase letters, numbers, and underscores.

- Valid Python identifiers. This is mostly handled by the rule above, but also prohibits names beginning with a digit; that is handled by prefixing those names with an underscore.

- Unique within the sheet. Non-unique names are suffixed with "__" and an integer.

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

This plugin adds one sheet command to VisiData:

- `normalize-col-names` normalizes the names of all *non-hidden* columns in the active sheet, per the approach described above. Alias: `normalize-column-names`.

See [the plugin file](plugins/normcol) for additional details.

## `tabulate`

This plugin makes it possible to save sheets as text-tables, using
the ["tabulate" library](https://bitbucket.org/astanin/python-tabulate).

The plugin adds two sheet commands to VisiData:

- `tabulate-copy` copies the sheet, as a text-table, to your clipboard
- `tabulate-save` saves the sheet, as a text-table, to file

It also adds one global option to VisiData:

- `tabulate_format` specifies the default text-table format. ([See here](https://bitbucket.org/astanin/python-tabulate#rst-header-table-format) for valid formats.)

See [the plugin file](plugins/tabulate) for additional details.

## `fec`

This plugin adds support for loading the Federal Election Commission's `.fec` files. In order for it to work, you'll need to install [fecfile](https://esonderegger.github.io/fecfile/): `pip install fecfile`. [Demo here](https://asciinema.org/a/Xyh2BFsUaOF0AlHTmMUbqQZPC).

See [the plugin file](plugins/fec) for additional details.
