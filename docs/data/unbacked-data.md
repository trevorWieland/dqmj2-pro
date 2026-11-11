# Unbacked data — address-space gaps and the roster find

Status: evidence report. Confidence: **proven-by-code** where marked; everything else is marked
unknown on purpose. No bytes are invented in this document.

Question: the data dictionary proves a 24-byte `species_roster` record at `0x021c4bf8` (species
`s16` at `+10`) from matched reader `native_main_0206d114`, but no captured module image covers that
address. This document maps the gaps, lists the readers found in matched source and in the image
literal scan, and states what would have to be captured to back the address.

## 1. Address-space map

Sources of truth: `manifest.json` (module base, image bytes, `bssStart`/`bssBytes`/`expectedBssBytes`)
and the extracted images under `extract/`. The ARM9 main RAM window is `0x02000000-0x023fffff`
(4 MiB); ITCM/DTCM and the ARM7 windows are separate.

### Backed by a captured image (file bytes exist)

| module | range | bytes | image |
| --- | --- | --- | --- |
| `main` | `0x02000000-0x020e3300` | 930,560 | `extract/arm9/arm9.bin` |
| `itcm` | `0x01ff8000-0x01fff8a0` | 30,880 | `extract/arm9/itcm.bin` |
| overlays `ov000`-`ov007` (union) | `0x021d7240-0x022300c0` | 364,160 (largest, `ov000`) | `extract/arm9_overlays/*.bin` |
| `dtcm` | `0x027e0000-0x027e0060` | 96 | `extract/arm9/dtcm.bin` |
| `arm7-boot` | `0x02380000-0x0238021c` | 540 | `extract/arm7/runtime/arm7-boot.bin` |

All eight overlays share base `0x021d7240` and are loaded one at a time; the union end is the
largest (`ov000`, `0x022300c0`). `utility-child-arm9-main` also uses base `0x02000000` but is a
different program (`dwc/utility.bin` child SRL) that aliases the same addresses when it runs; it is
not part of the main program's backing.

### Identified BSS (zero-filled at load, never file-backed)

| module | range | bytes | evidence |
| --- | --- | --- | --- |
| `main` | `0x020e3300-0x021d7240` | **999,232** | `manifest.json` `expectedBssBytes: 999232`; the size equals the whole main-to-overlay distance exactly |

This is the important correction to the earlier "gap" wording: **`0x020e3300-0x021d7240` is main's
BSS, not missing data.** Its size is recorded in the manifest and matches the address distance to
the byte (`0x021d7240 - 0x020e3300 = 0xf3f40 = 999,232`). `0x021c4bf8` therefore sits at offset
`0xe18f8` into main BSS, `0x12648` bytes before the overlay base.

Overlay BSS is not recorded (`bssStart` is `null` for every overlay), so whether an overlay extends
past its image end is **unknown**; it is not claimed either way.

### Not backed by any captured image

| range | bytes | note |
| --- | --- | --- |
| `0x01fff8a0-0x02000000` | 1,888 | between ITCM end and main base |
| `0x022300c0-0x02380000` | 1,376,064 | between the overlay union end and `arm7-boot` |
| `0x0238021c-0x02400000` | 523,748 | after `arm7-boot` to the end of main RAM |

These three ranges have no module at all: no image, no recorded BSS owner. They are ordinary RAM
from the hardware's point of view, but nothing in the manifest claims them, so no dump tool can
attribute bytes there yet.

### Why this matters for `species_roster`

`public_tools/data_dump.py` requires the target address to live inside a manifest module image
(`no-image` refusal). `0x021c4bf8` fails that test for two independent reasons: it is beyond the
main image end, and it belongs to main BSS, whose contents are not file-backed at all. An
additional image covering the range is therefore **necessary but not sufficient** — a *static* image
of main BSS cannot exist; the bytes only exist after the program has run and populated them.

## 2. The reader — found, and it is in the gap

The data dictionary's reader is matched in `src/mechanics_save/20261030_roster_frame_mask.c` as
`native_main_0206d114`. It indexes a 24-byte stride array at `0x021c4bf8`, which is inside main BSS
(the gap above). Per the hunt rule, that base falling in an unbacked gap **is the find**.

Matched sources that reference the roster base:

| source | symbol | evidence |
| --- | --- | --- |
| `src/mechanics_save/20261030_roster_frame_mask.c` | `native_main_0206d114` | `native_data_021c4bf9[sprite * 24]` (count), `native_data_021c4bfa[sprite * 24]` (first), `native_data_021c4bf8[sprite]` (record) |
| `src/mechanics_save/20261030_roster_species_predicate.c` | `native_main_0206db00` | `native_data_021c4bf8[sprite].species` compared against 139/176/188/254/350/425/426 |
| `src/runtime/runtime07/native_main_0206d23c.c` | `native_main_0206d23c` | `return 0x18 * arg0 + (s32)native_data_021c4bf8;` (row getter, stride 24 proven again) |
| `src/runtime/runtime09/native_main_0206d230.c` | `native_main_0206d230` | returns the base address itself; called from ov001 drafts |

Matched source alone therefore proves the address and the stride. To find candidate *writers* (needed
for capture), the main image was scanned for the literal word `0x021c4bf8` and its immediate
neighbours (`0x021c4bf9`, `0x021c4bfa`, `0x021c4af4`, `0x021c4afc`, `0x021c4b74`). Eleven functions
reference the roster base:

| literal site | containing function | matched | role |
| --- | --- | --- | --- |
| `0x0206c6b0` | `func_0206c644` | no | **initializer**: `memset(0x021c4bf8, 0, 360)` via `0x2008d78` |
| `0x0206c874` | `func_0206c718` | no | candidate writer |
| `0x0206ce44` | `func_0206ccb4` | no | candidate writer |
| `0x0206cf3c` | `func_0206ce54` | yes | reader |
| `0x0206cfdc` | `func_0206cf44` | no | candidate writer |
| `0x0206d078` | `func_0206cfe4` | no | reads the same count/first/pointer-array fields; candidate writer |
| `0x0206d10c` | `func_0206d080` | no | candidate writer |
| `0x0206d228` | `func_0206d114` | yes | the dictionary reader |
| `0x0206d238` | `func_0206d230` | yes | base getter |
| `0x0206d24c` | `func_0206d23c` | yes | row getter |
| `0x0206d90c` | `func_0206d838` | no | candidate writer |

Hard evidence from the initializer: `func_0206c644` zeroes the roster from `0x021c4bf8` for **360
bytes**, i.e. **15 records of 24 bytes**. That capacity figure is new relative to the data
dictionary (which only proved the stride). The same function also clears bytes at
`0x021c4af4`/`0x021c4afc` and the pointer array at `0x021c4b74`, which is consistent with the
neighbouring roster bookkeeping state.

The seven unmatched functions above are **candidates**, not proven writers: the scan proves they
reference the address, not the direction of the reference. `func_0206c644` is proven to write
(zero-fill); `func_0206cfe4` repeats the frame-mask read pattern.

## 3. Capture recommendation

### What cannot work

* A static slice of any existing image: main ends at `0x020e3300`, and the address is BSS.
* `dsd` alone: `tools/dsd.exe` extracts ROM contents and overlays (`extract/files/` already holds
  NitroFS files such as `ActTbl.bin`, `AbilityTbl.bin`). It cannot extract runtime RAM, and no
  extracted file is proven to correspond to `0x021c4bf8`. Whether the roster is ultimately copied
  from a NitroFS file is **unknown**.

### Recommended capture (primary)

Capture main RAM from a running game after the roster has been populated, then treat the BSS as a
pseudo-module:

1. Run the ROM (`inputs/game.nds`, SHA-256 recorded in `manifest.json`) under an emulator that can
   dump the 4 MiB main-RAM window, or load `inputs/save.sav` and reach the monster-roster screen.
2. Dump `0x02000000-0x023fffff` to `extract/arm9/main-ram.bin`.
3. Slice the BSS window `0x020e3300-0x021d7240` (999,232 bytes) to `extract/arm9/main-bss.bin`.
4. Record the capture provenance (emulator and version, ROM SHA-256, save SHA-256, scene reached,
   dump timestamp) next to the file; never commit the dump itself.
5. Add a manifest module `main-bss` with `base: 0x020e3300`, `bytes: 999232`,
   `binary: extract/arm9/main-bss.bin` and no BSS of its own.
6. Make the table resolvable by `public_tools/data_dump.py`, which today looks up exactly one
   module (`manifest_module(root, table['module'])`) and requires the address to fall inside that
   module's image. Two equivalent ways: point the `species_roster` index entry at the new
   `main-bss` module (address `0x021c4bf8` unchanged), or relax the lookup to select any manifest
   module whose range covers the address. With either, `--count 15` returns the 15 × 24-byte
   records from the captured BSS.

This backs every mechanics table in the same BSS block at once (`0x021c48f8`-`0x021c4fe4`), not just
the roster, which is why the whole-BSS dump is preferable to a narrow slice.

### Alternative capture (secondary, no emulator)

Trace the initializer chain (`func_0206c644` and the six candidate writers) to find where the record
bytes come from. Two outcomes are possible and currently **unproven**:

* copied from the save buffer: then `inputs/save.sav` plus the writer code yields the roster without
  a RAM dump, but the save offset is **unknown** today;
* copied/decoded from a NitroFS file: then `tools/dsd.exe` extraction plus the loader code yields the
  source table, but which file is **unknown** today.

Do not assume either. The literal scan gives the function list to disassemble next; the direction of
each reference must be established before it is called a loader.

## 4. Open unknowns

* Overlay BSS size/location (manifest records none) — whether overlays extend past their images is
  unknown.
* The six candidate writers' direction and data source.
* Whether the roster is populated from save data, from a NitroFS file, or built procedurally.
* The three genuinely unowned ranges (`0x01fff8a0-0x02000000`, `0x022300c0-0x02380000`,
  `0x0238021c-0x02400000`): no evidence yet that they hold static data rather than heap/stack.
