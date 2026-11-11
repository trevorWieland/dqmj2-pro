# Species and roster records

Index entries: `species_roster`. Confidence: **proven-by-code**.

## Roster slot record — `main` `0x021c4bf8`

The roster array is addressed as `native_data_021c4bf8[sprite]`; two matched files
declare their own view of one record. Both views are 24 bytes, so the stride is proven
even though the two structs name their bytes differently.

| offset | width | type | name | confidence | evidence |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | u8 | padding | inferred | declared in `src/mechanics_save/20261030_roster_frame_mask.c`; no matched reader |
| 1 | 1 | u8 | count | proven-by-code | `src/mechanics_save/20261030_roster_frame_mask.c` (`native_main_0206d114` reads `native_data_021c4bf9[sprite * 24]`) |
| 2 | 1 | s8 | first | proven-by-code | `src/mechanics_save/20261030_roster_frame_mask.c` (`native_main_0206d114` reads `native_data_021c4bfa[sprite * 24]`) |
| 3 | 21 | u8[21] | tail | unknown | declared, no matched reader |
| 10 | 2 | s16 | species | proven-by-code | `src/mechanics_save/20261030_roster_species_predicate.c` (`native_main_0206db00`) |

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

## Runtime-observed records (2026-11-11)

First real capture of this table: `work/emulator/dumps/switch-open.bin` (spec
`work/emulator/specs/roster-6.json`; dump sha256
`16b4899f1b7393551d147cea1efe2b9744781ea59a21a83c25337b0911ef8d2f`; roster slice
`extract/ram/ram-roster_021c4bf8.bin`, sha256
`cd20f431c18abc45716b35ab1ea5f30b76e189d3c762239bbc1126cc14e4f2a0`). Captured with
DeSmuME 0.9.13 through `ops/emulate_capture.py`; procedure and provenance in
`docs/data/runtime-capture.md`.

The **Switch Monsters** screen (X menu → page to "Switch Monsters" → A) populated
**6 of the 15 slots**; slots 6-14 are zero because the save owns six monsters (three
party, three reserve), not because the capture failed.

| slot | species (+0x0A) | id (+0x04) | +0x0C | pointer (+0x10) | pointer (+0x14) |
| --- | --- | --- | --- | --- | --- |
| 0 | 263 | 32 | 0 | `0x023a9b6c` | `0x023a9ecc` |
| 1 | 403 | 832 | 1 | `0x023ad444` | `0x023aa03c` |
| 2 | 403 | 1632 | 1 | `0x023af284` | `0x023aa1ac` |
| 3 | 65 | 2432 | 0 | `0x023af5e4` | `0x023ad8e4` |
| 4 | 260 | 3232 | 0 | `0x023af9e4` | `0x023ad9b4` |
| 5 | 405 | 4032 | 0 | `0x023afe84` | `0x023ad9e4` |

Slot 0 bytes:
`00 01 00 01 20 00 00 00 ff 00 07 01 00 00 00 00 6c 9b 3a 02 cc 9e 3a 02`.

Reading, all **runtime-observed** unless noted:

* `+0x01` = 1 and `+0x02` = slot number (0-5), matching the proven `count`/`first`
  readers; `+0x0A` species matches the screen: slot 0 Nighty, slots 1-2 ConkaI and
  ConkaII (both 403), slots 3-5 the three reserve monsters.
* `+0x04` is a 32-bit id with a fixed **800-byte (0x320) stride**: 32, 832, 1632, 2432,
  3232, 4032. 800 bytes is the per-monster allocation stride, so this is a monster
  handle, not the list index.
* `+0x08` = `0xFF`, `+0x09` = 0, `+0x10` and `+0x14` are heap pointers to **preview
  graphics resources** (`0x023Axxxx`), not to monster stat objects — see
  "Runtime-observed monster object" below. The 24-byte record is therefore a
  **reference/index** entry: it carries species, slot order and preview pointers, and
  no stats at all.
* `+0x0C` is 1 for slots 1-2 (both species 403) and 0 for slots 0, 3, 4, 5. No matched
  reader explains it; its meaning is undetermined.

Species values **263, 403, 65, 260, 405** are now runtime-observed. They are outside
the seven-value comparison set above (139/176/188/254/350/425/426), which is a
predicate for "special sprite", not a species enumeration; the observation does not
contradict it.

Capacity caveat: 15 slots is the array capacity (15 x 24 = 360 B). Filling all 15 needs
a save that owns 15 monsters; this save does not, so the remaining records stay zero.

## Runtime-observed monster object (800 bytes)

**Status: runtime-observed, not code-proven.** Every offset below was found by matching
captured bytes against values the game itself printed on the Switch Monsters screen; no
matched reader for this object has been found yet. Treat the names as strong hypotheses
and the offsets as measured.

Located by value scan in the 4 MiB capture (`work/emulator/dumps/heap-4m.bin`, sha256
`06fed5d54996cba293c2b9527b1bd3ffed35f20f61a73fa6b1f2c24785b68adb`). One object per
owned monster, `0x320` (800) bytes apart — the same stride as the roster record's
`+0x04` id, which is why that id looks like an allocation handle:

| object | address | species | source |
| --- | --- | --- | --- |
| Nighty | `0x021bd710` | 263 | party slot 0 |
| ConkaI | `0x021be91c` | 403 | party slot 1 |
| ConkaII | `0x021bea24` | 403 | party slot 2 |
| reserve | `0x021bf36c` | 65 | storage |
| reserve | `0x021bf3f0` | 260 | storage |
| reserve | `0x021bf474` | 405 | storage |

### Fields

u16 little-endian except Exp (u32). Sample values are from the six captured objects;
"screen" means the game's own display at capture time.

| offset | name | type | Nighty | ConkaI | ConkaII | res 65 | res 260 | res 405 | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| +0x00 | species | u16 | 263 | 403 | 403 | 65 | 260 | 405 | high — matches record +0x0A and screen |
| +0x08 | HP base | u16 | 1000 | 832 | 832 | 274 | 179 | 183 | medium — max minus equipment |
| +0x0A | MP | u16 | 260 | 450 | 450 | 56 | 58 | 84 | high — exact screen match |
| +0x0C | HP max | u16 | 1100 | 892 | 892 | 274 | 179 | 183 | high — exact screen match |
| +0x0E | MP max | u16 | 260 | 450 | 450 | 56 | 58 | 84 | high — duplicate of +0x0A in all six |
| +0x10 | Attack base | u16 | 1000 | 787 | 787 | 211 | 226 | 190 | medium — screen adds equipment |
| +0x12 | Defence base | u16 | 986 | 900 | 900 | 224 | 157 | 172 | medium — screen adds equipment |
| +0x14 | Agility | u16 | 261 | 1012 | 1012 | 124 | 142 | 139 | high — exact screen match |
| +0x16 | Wisdom | u16 | 320 | 765 | 765 | 161 | 152 | 91 | high — exact screen match |
| +0x1C | Exp | u32 | 6684744 | 3553483 | 3434250 | 4181 | 4181 | 4181 | high for Nighty (exact); other rows unverified |

The three reserves have base == max on every pair, which is the strongest evidence that
`+0x08` is unequipped HP and `+0x0C` is equipped max HP: storage monsters carry no gear.

### Unresolved

* **Level has no byte field.** No `97`/`99` byte or u16 appears anywhere in Nighty's or
  ConkaI's 800-byte object. ConkaI and ConkaII have identical stats, yet display Lv★ and
  Lv97, and differ only at `+0x02`, `+0x04`, `+0x06` and Exp. Most likely level is
  derived from Exp at `+0x1C`; do not add a level field without new evidence.
* **Displayed stats are sometimes derived.** Nighty's screen shows Attack 1200 and
  Defence 991, but the object stores 1000 and 986. The gap is equipment (Gae Bolg:
  +200 Attack, +5 Defence). A search for 1200 (`0x04B0`) finds no candidate in the
  object or in the whole 4 MiB — compare base fields, never screen values.
* `+0x02`, `+0x04`, `+0x06` and everything after `+0x1C` are not interpreted.

### Negative result: the 24-byte record is a reference entry only

The roster record's `+0x10`/`+0x14` pointers do **not** point at these objects. Every
dereferenced target starts with graphics-resource magic — `52 47 43 4e` ("RGCN",
byte-swapped NCGR) then `52 41 48 43` ("RAHC") — i.e. tileset/cell data for the menu
preview. The 24-byte array is an index/presentation entry: species, slot order and
preview resource pointers, and no stats. Do not re-derive this by assuming the pointers
are monster handles; the stat objects are found by value (or by the id stride), not by
following the record.

Raw evidence: `work/emulator/objects/` (six 800-byte object dumps, twelve pointer
slices, `objects.json`, `struct-report.json`).

## What is deliberately absent

* **Per-species base-stat tables** (HP/attack/defence/agility for each species id):
  the six captured objects give per-monster values; no species table is proven.
* **Growth curves**: no matched reader exists.
* **Encounter tables**: no matched reader exists.

See `index.json` -> `unknown_families`. Nothing is listed for them because no address is
established; inventing one would make the dictionary worse than empty.

## Dump status

`public_tools/data_dump.py --table species_roster` refuses this table today: the address
is proven by the symbol name in matched source, but no *static* module image covers it.
The main ARM9 image ends at `0x020E3300` and the overlay images start at `0x021D7240`, so
`0x021C4BF8` sits in a gap between captured module images.

`ops/ram_capture.py` now produces exactly such an image:
`extract/ram/ram-roster_021c4bf8.bin` (360 B, `kind: runtime-capture`) with a manifest
entry pointing at `0x021c4bf8`. The monster objects are not part of that image either -
they live in heap at `0x021Bxxxx`-`0x021Cxxxx`, inside the full 4 MiB main-RAM window
that `ops/emulate_capture.py --dump-length 4194304` captures.
