# Worked example — a one-byte title edit with checksum fix-up

This is the smallest complete mod: change the ROM title's last character, fix the
header CRC, and write a new image. It is deliberately cosmetic — the title is what
the DS firmware and most emulators show in their file list — so the example proves
the whole patch pipeline without touching game logic.

## The change

The header title occupies ROM offsets `0x000`–`0x00B`, twelve ASCII bytes:

```
before  D Q M - J O K E R 2 - P      = 44 51 4d 2d 4a 4f 4b 45 52 32 2d 50
after   D Q M - J O K E R 2 - M      = 44 51 4d 2d 4a 4f 4b 45 52 32 2d 4d
```

So the patch is one byte, at file offset `0x00B`: `0x50` -> `0x4D`.

## The spec

[`example-title.json`](example-title.json):

```json
{
  "input": "inputs/game.nds",
  "output": "build/mods/title/game-title.nds",
  "fixHeaderChecksum": true,
  "patches": [
    {
      "offset": "0x00B",
      "before": "50",
      "after": "4D",
      "note": "ROM title, last character: 'P' -> 'M' (DQM-JOKER2-P -> DQM-JOKER2-M)"
    }
  ]
}
```

The `before` byte is what makes the spec safe: it is checked against the image
first, and the tool refuses to write anything if the byte differs.

## Commands and expected output

Verify without writing:

```
> python ops/mod_patch.py --spec docs/modding/example-title.json --dry-run
input      ...\inputs\game.nds (175959612 bytes)
checksum   stored 0x82cd  computed 0x82cd  match
patch 0  0x00000b  1 B  ok  (ROM title, last character: 'P' -> 'M' (DQM-JOKER2-P -> DQM-JOKER2-M))
checksum   written 0x83a9
header     valid after patch (logo CRC, header CRC, field bounds)
--dry-run: patches verified, nothing written
```

Write the image:

```
> python ops/mod_patch.py --spec docs/modding/example-title.json
...
wrote ...\build\mods\title\game-title.nds (175959612 bytes)
```

Validate the result with the repository's own header rules:

```
> python ops/mod_patch.py --verify-header build/mods/title/game-title.nds
header valid: logo CRC ok, header CRC 0x83a9, fields in range
```

The only bytes that differ between the input and the output are `0x00B` and the
two header-CRC bytes at `0x15E`–`0x15F`.

## Checksum arithmetic

The header CRC is **CRC-16/ARC** (polynomial `0xA001` reflected, initial `0xFFFF`)
over bytes `0x000..0x15D`, stored little-endian at `0x15E` — the same function the
repository validator uses (`audit_regions.py`, `nds_header`, via
`ndspy._common.crc16`; also `utility_runtime.py:180`).

- unmodified image: CRC-16 = `0x82CD`, and the stored value is `0x82CD` → the
  header is valid and the input image is pristine;
- after changing `0x0B` from `0x50` to `0x4D`, the CRC-16 is `0x83A9`.

A CRC is **not** linear, so there is no "delta" reasoning here: the new value has
to be computed over the whole header, which is what the tool does. (An earlier
revision of this document used a byte-sum formula and reported `0x9FD4`/`0x9FD7`;
that was the wrong algorithm and would have produced a non-booting image. The
0x82CD stored in the input is exactly what CRC-16 produces, which is how the
error was caught.)

## How to check the result

1. `--verify-header` on the output must pass (logo CRC, header CRC, field bounds),
   and it does: `header CRC 0x83a9`.
2. The same spec run against the untouched input must pass its before-byte checks;
   a spec with a deliberately wrong `before` must fail with exit 1 and write
   nothing.
3. A spec whose `output` resolves to the input must be refused — the tool exits 1
   with "refusing to overwrite it in place".
4. The output size must equal the input size exactly (175,959,612 bytes); this mod
   changes no offsets.
5. Boot it in an emulator: the title in the file list reads `DQM-JOKER2-M`. Any
   save file from the unmodified image still loads, because nothing in the payload
   moved.

## What this example does not prove

It does not touch the game payload at all. Editing a data table is a different
lane: `docs/data/index.json` records runtime addresses, and `species_roster`
(`0x021C4BF8`) is not even inside a loaded module image — it sits between the end
of main (`0x020E3300`) and the overlay base (`0x021D7240`). Tables that *are* inside
the ARM9 module are additionally stored **compressed** in the ROM. See the parent
`README.md`.

## Reproducing with a different ROM revision

Change the `before` byte to whatever the target image actually holds at `0x00B`,
or the tool will refuse. That refusal is the feature: a spec written for this image
must never be applied silently to another one.
