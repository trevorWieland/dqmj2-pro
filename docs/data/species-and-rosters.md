# Species and roster records

Index entries: `species_roster`. Confidence: **proven-by-code**.

## Roster slot record — `main` `0x021c4bf8`

The roster array is addressed as `native_data_021c4bf8[sprite]`; two matched files
declare their own view of one record. Both views are 24 bytes, so the stride is proven
even though the two structs name their bytes differently.

| offset | width | type | name | confidence | evidence |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | u8 | padding | proven-by-code | `src/mechanics_save/20261030_roster_frame_mask.c` |
| 1 | 1 | u8 | count | proven-by-code | `src/mechanics_save/20261030_roster_frame_mask.c` |
| 2 | 1 | s8 | first | proven-by-code | `src/mechanics_save/20261030_roster_frame_mask.c` |
| 3 | 21 | u8[21] | tail | unknown | declared, no matched reader |
| 10 | 2 | s16 | species | proven-by-code | `src/mechanics_save/20261030_roster_species_predicate.c` |

`sprite` indexes the record (`native_main_0206db00`), and the species value is compared
against 139, 176, 188, 254, 350, 425 and 426 to answer "is this a special sprite". That
comparison is the only proven meaning of the field: it is a species identifier, but
which species each number denotes is not established by code.

The two views overlap deliberately: `src/mechanics_save/20261030_roster_species_predicate.c`
declares `{ u8 prefix[10]; s16 species; u8 tail[12]; }` while
`src/mechanics_save/20261030_roster_frame_mask.c` declares
`{ u8 padding; u8 count; s8 first; u8 tail[21]; }`. Both are 24 bytes and both are
matched, so a reader must not assume a single canonical name for offsets 0-9 beyond the
fields listed above.

## What is deliberately absent

* **Species stats** (HP/attack/defence/agility per species): no matched reader exists.
* **Growth curves**: no matched reader exists.
* **Encounter tables**: no matched reader exists.

See `index.json` → `unknown_families`. Nothing is listed for them because no address is
established; inventing one would make the dictionary worse than empty.

## Dump status

`public_tools/data_dump.py --table species_roster` refuses this table today: the address is
proven by the symbol name in matched source, but **no module image covers it**. The main
ARM9 image ends at `0x020E33C0` and the overlay images start at `0x021D7240`, so
`0x021C4BF8` sits in a gap between captured module images. Dumping it needs an image that
covers the range; the dictionary reports the address rather than inventing bytes.
