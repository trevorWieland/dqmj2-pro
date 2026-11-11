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
* `+0x08` = `0xFF`, `+0x09` = 0, `+0x10` and `+0x14` are heap pointers into the live
  monster objects (`0x023Axxxx`). The 24-byte record is therefore a **reference**
  entry: level, HP, MP and stats live behind those pointers (the screen showed Nighty
  at HP 1100, Attack 1200, Rank S+16) and are *not* stored in these 24 bytes.
* `+0x0C` is 1 for slots 1-2 (both species 403) and 0 for slots 0, 3, 4, 5. No matched
  reader explains it; its meaning is undetermined.

Species values **263, 403, 65, 260, 405** are now runtime-observed. They are outside
the seven-value comparison set above (139/176/188/254/350/425/426), which is a
predicate for "special sprite", not a species enumeration; the observation does not
contradict it.

Capacity caveat: 15 slots is the array capacity (15 x 24 = 360 B). Filling all 15 needs
a save that owns 15 monsters; this save does not, so the remaining records stay zero.

## Where the monster stats actually live (follow-up, 2026-11-11)

A 4 MiB capture (`0x02000000`-`0x02400000`, `work/emulator/dumps/heap-4m.bin`) was
taken at the same Switch Monsters state to follow `+0x10`/`+0x14`. Result: those two
pointers are **not** monster stat objects. Every dereferenced target begins with
graphics-resource magic — `52 47 43 4e` ("RGCN", byte-swapped NCGR) followed by
`52 41 48 43` ("RAHC") — i.e. tileset/cell data used for the preview, not stats. The
24-byte record is a *presentation/reference* entry for menu rendering.

The real monster objects were instead located by value in the same dump, and they sit
elsewhere in main RAM: Nighty at `0x021bd710`, ConkaI at `0x021be91c`, ConkaII at
`0x021bea24`, reserves at `0x021bf36c` / `0x021bf3f0` / `0x021bf474`. Each object is
`0x320` bytes (the same 800-byte stride as the id at record `+0x04`). Candidate layout,
u16 little-endian from the object base:

| offset | field | evidence | confidence |
| --- | --- | --- | --- |
| +0x00 | species | 263, 403, 65, 260, 405; matches record `+0x0A` and the screen | high |
| +0x08 | HP (unequipped) | 1000 for Nighty vs 1100 shown with equipment | medium |
| +0x0A | MP | 260 / 450 / 56 / 58 / 84 exactly match the screen | high |
| +0x0C | HP (max, equipped) | 1100 and 892 exactly match HP max on screen | high |
| +0x0E | MP (max) | duplicate of +0x0A in all six | high |
| +0x10 | Attack (unequipped) | 1000 for Nighty; screen shows 1200 with "Gae Bolg" | medium |
| +0x12 | Defence (unequipped) | 986; screen shows 991 (+5) | medium |
| +0x14 | Agility | 261 exactly matches the screen | high |
| +0x16 | Wisdom | 320 exactly matches the screen | high |
| +0x1C | Exp (u32) | 6,684,744 exactly matches Nighty's Exp | high |

Nighty's displayed **1200 Attack and 991 Defence are not stored anywhere in the
object** — the object holds 1000 and 986, and the displayed values include equipment
bonuses (Gae Bolg: +200 Attack, +5 Defence). A raw search of the whole 4 MiB finds no
`0x04B0` (1200) in Nighty's object.

**Level was not found as an explicit field.** No byte `97`/`99` (or u16) appears in
Nighty's or ConkaI's object; ConkaI and ConkaII share identical stats yet display Lv★
and Lv97, and differ only at `+0x02`, `+0x04`, `+0x06` and Exp. The most likely model is
that level is derived from Exp at `+0x1C`, not stored. Treat the level question as open.

Raw slices and the annotated report are under `work/emulator/objects/`
(`struct_*.bin`, `struct-report.json`, `objects.json`).

## What is deliberately absent

* **Species stats** (HP/attack/defence/agility per species): no matched reader exists.
* **Growth curves**: no matched reader exists.
* **Encounter tables**: no matched reader exists.

See `index.json` → `unknown_families`. Nothing is listed for them because no address is
established; inventing one would make the dictionary worse than empty.

## Dump status

`public_tools/data_dump.py --table species_roster` refuses this table today: the address is
proven by the symbol name in matched source, but **no module image covers it**. The main
ARM9 image ends at `0x020E3300` and the overlay images start at `0x021D7240`, so
`0x021C4BF8` sits in a gap between captured module images. Dumping it needs an image that
covers the range; the dictionary reports the address rather than inventing bytes.

`ops/ram_capture.py` now produces exactly such an image: `extract/ram/ram-roster_021c4bf8.bin`
(360 B, `kind: runtime-capture`) with a manifest entry pointing at `0x021c4bf8`. See
`docs/data/runtime-capture.md`.
