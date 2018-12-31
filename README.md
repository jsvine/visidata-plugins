# Custom VisiData Plugins

This repository serves as a place for me to share VisiData plugins I've written. Currently, there's just one.

All code is released under the MIT License.

## `vddedupe.py`

This plugin adds two sheet commands to VisiData:

- `select-duplicate-rows` sets the selection status in VisiData to `selected` for each row in the active sheet that is a duplicate of a prior row.

- `dedupe-rows` pushes a new sheet in which only non-duplicate rows in the active sheet are included.

See [the plugin file](plugins/vddedupe.py) for usage details.
