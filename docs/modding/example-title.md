# Worked example — a one-byte title edit with checksum fix-up

This is the smallest complete mod: change the ROM title's last character, fix the
header checksum, and write a new image. It is deliberately cosmetic — the title is
what the DS firmware and most emulators show in their file list — so the example
proves the whole patch pipeline without touching game logic.

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
input      inputs\game.nds (175959612 bytes)
checksum   stored 0x82cd  computed 0x9fd4  MISMATCH
patch 0  0x00000b  1 B  ok  (ROM title, last character: 'P' -> 'M' (DQM-JOKER2-P -> DQM-JOKER2-M))
checksum   written 0x9fd7
--dry-run: patches verified, nothing written
```

Write the image:

```
> python ops/mod_patch.py --spec docs/modding/example-title.json
input      inputs\game.nds (175959612 bytes)
checksum   stored 0x82cd  computed 0x9fd4  MISMATCH
patch 0  0x00000b  1 B  ok  (ROM title, last character: 'P' -> 'M' (DQM-JOKER2-P -> DQM-JOKER2-M))
checksum   written 0x9fd7
wrote build/mods/title/game-title.nds (175959612 bytes)
```

The only bytes that differ between the input and the output are `0x00B` and the
two checksum bytes at `0x15E`–`0x15F`.

## Checksum arithmetic

The checksum is `(0x10000 - ((sum(bytes[0:0x15E]) + 0x55) & 0xFFFF)) & 0xFFFF`.
Changing `0x50` to `0x4D` lowers the byte sum by `0x03`, so the written checksum
rises by `0x03`: `0x9FD4` -> `0x9FD7`.

Note the input image's **stored** checksum (`0x82CD`) does not equal the formula's
result (`0x9FD4`), so the input is not a pristine retail dump. The tool always
recomputes; do not trust the stored value in the input.

## How to check the result

1. `--check` on a spec that expects the *new* bytes must pass, and the same spec
   run against the untouched input must fail at the before-byte check. That is the
   regression that proves the guard works.
2. The output size must equal the input size exactly (175,959,612 bytes); this mod
   changes no offsets.
3. Boot it in an emulator: the title in the file list reads `DQM-JOKER2-M`. Any
   save file from the unmodified image still loads, because nothing in the payload
   moved.

## What this example does not prove

It does not touch the game payload at all. Editing a data table — species rosters,
skills, items — means editing the ARM9 image, which is stored **compressed** in the
ROM (607,328 stored bytes expanding to 961,560). That is the rebuild lane, not the
patch lane; see the parent `README.md`.

## Reproducing with a different ROM revision

Change the `before` byte to whatever the target image actually holds at `0x00B`,
or the tool will refuse. That refusal is the feature: a spec written for this image
must never be applied silently to another one.
