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

Both come from `manifest.json` (`rom`), and the extracted modules are bound to the
same hash (`buildSha256` in `public/accepted-functions.json`). **A patch spec is
only valid for an image with exactly this hash** — that is the whole point of the
before-bytes requirement in `ops/mod_patch.py`.

## Measured section layout

Read from the header of the image above (offsets are ROM file offsets, sizes are
bytes):

| field | header offset | value |
| --- | --- | --- |
| title | `0x000` | 12 bytes ASCII (`DQM-JOKER2-P`) |
| game code | `0x00C` | `B2JJ` |
| ARM9 ROM offset / size | `0x020` / `0x02C` | `0x4000` / `0x94460` |
| ARM9 **entry point** | `0x024` | `0x02000800` |
| ARM9 **load (RAM) address** | `0x028` | `0x02000000` |
| ARM7 ROM offset / size | `0x030` / `0x03C` | `0x98800` / `0x27130` |
| ARM7 entry point | `0x034` | `0x02380000` |
| FNT offset / size | `0x040` / `0x044` | `0xBFA00` / `0x5351` |
| FAT offset / size | `0x048` / `0x04C` | `0xC4E00` / `0x36D8` (1,755 entries) |
| overlay table offset / size | `0x050` / `0x054` | `0x98600` / `0x100` |
| logo CRC | `0x15C` | CRC-16 over bytes `0xC0..0x15B` |
| header CRC | `0x15E` | CRC-16 over bytes `0x000..0x15D` |

Note the distinction between the two ARM9 addresses, which is easy to confuse:
`0x020` says where the image is **stored in the file**, `0x024` is the **entry
point** (first instruction executed, `0x02000800`), and `0x028` is the address the
image is **loaded at** (`0x02000000`). A runtime address `A` inside the ARM9 module
maps to file offset `arm9_rom_offset + (A - 0x02000000)`.

## Module extents, and the gap that matters for table edits

| module | base | size | end |
| --- | --- | --- | --- |
| itcm | `0x01FF8000` | 30,880 | `0x01FFF8A0` |
| main | `0x02000000` | 930,560 | `0x020E3300` |
| ov000…ov006 | `0x021D7240` | per overlay | — |
| arm7-main | `0x027E0000` | 96,388 | `0x027F7884` |

`docs/data/index.json` records `species_roster` at `0x021C4BF8`. That address is
**above the end of the main module (`0x020E3300`)** and **below the overlay base
(`0x021D7240`)**, so it does not fall inside the ARM9 image at all — it sits in an
uncovered gap whose runtime backing the project has not yet proven. It is therefore
neither patchable nor rebuildable today: the table's existence and layout are
`proven-by-code` from the functions that read it, but nothing yet says what memory
holds it in the shipped image.

Separately, the ARM9 image **is** stored compressed in the ROM (607,328 stored bytes
expanding to 961,560, with overlay 004 additionally DSProtect-encrypted — see
`docs/2026-10-27-reconstruction.md`). So a table that *is* inside the ARM9 module
still cannot be reached by file offset: those bytes are compressed.

So there are three lanes:

1. **Patch lane (documented here):** header fields and any uncompressed byte range,
   with a checksum fix-up. `ops/mod_patch.py` implements it.
2. **Rebuild lane:** tables and function bodies inside the ARM9/overlay images,
   which requires rebuilding and repacking (`pack_exact.py`, `rom_layout.py`,
   DSProtect serialisation) — the project's own build path, out of scope here.
3. **Unbacked addresses:** like `species_roster`, proven by the code that reads them
   but not yet located in the shipped image.

## Header checksum

The DS header carries **CRC-16** values, not byte sums. Both are computed with
polynomial `0xA001` (reflected CRC-16/ARC), initial value `0xFFFF`:

- logo CRC at `0x15C` over bytes `0xC0..0x15B`;
- **header CRC at `0x15E` over bytes `0x000..0x15D`**.

This matches the repository's own validator (`audit_regions.py`, `nds_header`,
which uses `ndspy._common.crc16` for both fields) and `utility_runtime.py:180`. On
the provided image the stored `0x15E` is `0x82CD` and the CRC-16 of
`0x000..0x15D` is exactly `0x82CD`, so the input header is **valid and pristine**.
`ops/mod_patch.py` recomputes the header CRC after patching and refuses to write an
image whose header would not validate.

## Worked example

See [`example-title.md`](example-title.md) and [`example-title.json`](example-title.json):
a one-byte title change plus checksum fix-up, with the exact commands, the real
before/after bytes and the validator output.

## What you can and cannot safely change today

What the data dictionary (`docs/data/index.json`) proves, and therefore what this
lane can talk about:

| table | address | status for a byte patch |
| --- | --- | --- |
| `species_roster` (stride 24) | `0x021C4BF8` | **unbacked address** — between main's end and the overlay base; not located in the image |
| `skill_records` (stride 60) | unknown | rebuild lane at best; address not proven |
| `item_descriptors` | unknown | rebuild lane at best; stride not proven |
| `save_money`, `save_bank_header`, `saved_record` | unknown | **save file**, not the ROM — different tooling entirely |
| `arm7_player_view` / `arm7_track_view` | `0x03808420` / `0x03808660` | inside the ARM7 image (rebuild lane) |
| `arm7_boot_parameters` | `0x02380204` | `inferred` confidence; above arm7-main's end — unbacked |
| `math_table_0x20d3fe0` | `0x020D3FE0` | inside the main module (rebuild lane) |

Safe today, with this tool:

- header fields: title (`0x000`–`0x00B`), and other header words once the before
  bytes are verified;
- the header CRC fix-up, which is required after any header edit;
- any byte range whose before bytes match, i.e. any *uncompressed* payload.

**Unavailable / do not attempt:**

- **Monster stats: unavailable.** The data dictionary has ten tables and none of
  them is a monster-stat, growth or encounter table; there is no proven address,
  stride or field layout for monster stats anywhere in the project yet.
- Experience, gold and item quantities: `save_money` is a **save-file** structure,
  not a ROM table, so a ROM patch cannot change starting money.
- Anything inside the ARM9/overlay images by file offset (compressed region).
- Any table whose address is not backed by a loaded module image
  (`species_roster`, `arm7_boot_parameters`).
- Checksums beyond the header: ROM payload and DSProtect container integrity are
  not recomputed by this tool, so patching bytes a protected container covers will
  produce an image that fails validation.

## Tool

```bash
python ops/mod_patch.py --spec docs/modding/example-title.json --check    # verify only
python ops/mod_patch.py --spec docs/modding/example-title.json            # write output
python ops/mod_patch.py --verify-header build/mods/title/game-title.nds   # validate a header
```

- the spec is JSON: `input`, `output`, `fixHeaderChecksum`, and `patches[]` with
  `offset`, `before` (hex), `after` (hex) and an optional `note`;
- every `before` is checked against the image first; on any mismatch the tool
  writes nothing and exits `1`, so a spec for one ROM revision cannot corrupt
  another;
- the output is always a **new** file; an output path that resolves to the input is
  refused (in-place editing is how a 512-byte test image gets destroyed);
- `--verify-header` mirrors the repository validator (logo CRC, header CRC, field
  bounds) and is run on the patched image before writing;
- the tool never stores or emits a ROM; only the spec and the commands are
  versioned.
