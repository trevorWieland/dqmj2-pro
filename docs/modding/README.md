# Modding the built image — patch surface, lens 1

This directory documents what a modder can safely change in the **built** ROM,
and what has to go through the rebuild path instead. It is deliberately narrow: it
describes the byte patch surface the project can prove, not a general modding SDK.

## The image this refers to

| property | value |
| --- | --- |
| path | `inputs/game.nds` |
| size | 175,959,612 bytes |
| SHA-256 | `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6` |

Both come from `manifest.json` (`rom`), and the checksum of the extracted modules
is bound to the same hash (`buildSha256` in `public/accepted-functions.json`).
**A patch spec is only valid for an image with exactly this hash** — that is the
whole point of the before-bytes requirement in `ops/mod_patch.py`.

## Measured section layout

Read from the header of the image above (all offsets are ROM file offsets, sizes
are bytes):

| field | offset / value |
| --- | --- |
| title | `0x000`, 12 bytes ASCII (`DQM-JOKER2-P`) |
| game code | `0x00C` (`B2JJ`) |
| header checksum | `0x15E`, 16-bit little-endian |
| ARM9 ROM offset / size | `0x4000` / `0x94460` |
| ARM9 load address | `0x02000800` |
| ARM7 ROM offset / size | `0x98800` / `0x27130` |
| ARM7 load address | `0x02380000` |
| FNT offset / size | `0xBFA00` / `0x5351` |
| FAT offset / size | `0xC4E00` / `0x36D8` (1,755 entries) |
| overlay table offset / size | `0x98600` / `0x100` |

## The patch target, and the reason most table edits cannot use it

A byte patch is only meaningful where the file content **is** the runtime content.
That is true for the header and for uncompressed regions. It is **not** true for the
ARM9 image or the overlays:

- `docs/2026-10-27-reconstruction.md` records the ARM9 module stored in the ROM at
  607,328 bytes decompressing to 961,560 bytes, with overlay 004 additionally
  DSProtect-encrypted.
- Every data table in `docs/data/index.json` is addressed by **runtime** address in
  the ARM9 image (for example `0x021c4bf8`), so a modder cannot reach it by file
  offset: the bytes at that location in the ROM are compressed.

So there are two lanes, and this deliverable covers only the first:

1. **Patch lane (documented here):** header fields and any uncompressed byte range,
   with a checksum fix-up. `ops/mod_patch.py` implements it.
2. **Rebuild lane (not covered):** changing a table or function body inside the
   ARM9/overlay images means rebuilding the image and repacking the container
   (`pack_exact.py`, `rom_layout.py`, DSProtect serialisation), which is the
   project's own build path and is out of scope for a modder-facing tool today.

## Header checksum

The DS header stores a 16-bit checksum at `0x15E`, computed over bytes
`0x000..0x15D`:

```
sum      = sum(bytes[0x000:0x15E]) & 0xFFFF
checksum = (0x10000 - ((sum + 0x55) & 0xFFFF)) & 0xFFFF
```

**Measured discrepancy in the provided image:** the stored value is `0x82CD` while
the formula over the file yields `0x9FD4`. The input image is therefore not a
pristine retail dump (or was patched without a checksum fix-up). `ops/mod_patch.py`
reports both values on every run and rewrites the field to the recomputed value
unless the spec sets `fixHeaderChecksum: false`. Do not assume the stored checksum
of the input is authoritative — recompute it.

## Worked example

See [`example-title.md`](example-title.md) and the spec next to it,
[`example-title.json`](example-title.json): a one-byte title change plus checksum
fix-up, with the exact commands and before/after bytes.

## What you can and cannot safely change today

What the data dictionary (`docs/data/index.json`) proves and therefore what this
lane can talk about:

| table | runtime address | status for a byte patch |
| --- | --- | --- |
| `species_roster` (stride 24) | `0x021c4bf8` | **rebuild lane** — inside the compressed ARM9 image |
| `skill_records` (stride 60) | unknown | rebuild lane; address not yet proven |
| `item_descriptors` | unknown | rebuild lane; stride not proven |
| `save_money`, `save_bank_header`, `saved_record` | unknown | **save file**, not the ROM — different tooling entirely |
| `arm7_player_view` / `arm7_track_view` | `0x03808420` / `0x03808660` | rebuild lane (ARM7 image) |
| `arm7_boot_parameters` | `0x02380204` | rebuild lane, `inferred` confidence only |
| `math_table_0x20d3fe0` | `0x020d3fe0` | rebuild lane, `inferred` confidence only |

Safe today, with this tool:

- header fields: title (`0x000`–`0x00B`), and other header words once you verify the
  before bytes;
- the header checksum fix-up, which is required after any header edit;
- any byte range whose before bytes match, i.e. any *uncompressed* payload.

**Unavailable / do not attempt:**

- **Monster stats: unavailable.** The data dictionary has ten tables and none of
  them is a monster-stat, growth or encounter table; there is no proven address,
  stride or field layout for monster stats anywhere in the project yet.
- Experience, gold and item quantities: `save_money` is a **save-file** structure,
  not a ROM table, so a ROM patch cannot change starting money.
- Anything inside the ARM9/overlay images by file offset (see above).
- Checksums beyond the header: the ROM payload checksum and DSProtect container
  integrity are not recomputed by this tool, so patching bytes that a protected
  container covers will produce an image that fails validation.

## Tool

```bash
python ops/mod_patch.py --spec docs/modding/example-title.json --check    # verify only
python ops/mod_patch.py --spec docs/modding/example-title.json            # write output
```

- the spec is JSON: `input`, `output`, `fixHeaderChecksum`, and `patches[]` with
  `offset`, `before` (hex), `after` (hex) and an optional `note`;
- every `before` is checked against the image first; on any mismatch the tool
  writes nothing and exits `1`, so a spec for one ROM revision cannot corrupt
  another;
- the output is always a **new** file, never an in-place edit;
- the tool never stores or emits a ROM; only the spec and the commands are
  versioned.
