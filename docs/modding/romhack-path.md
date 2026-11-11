# Romhack path — what is achievable today

Two halves decide whether a romhacker can change what the player sees: getting edit bytes back into
the ROM container, and knowing where the text actually lives. The first half is now solved; the
second is not, and this page names exactly what is missing rather than approximating it.

## Half 1 — container repack: PASS

`public_tools/fpk_repack.py` parses and repacks FPK archives without the pinned reader. Layout,
measured from the extract (see the module docstring for the byte-level description):

```
header        4 B magic "FPK\0" + 4 B member count
member table  count x 0x28 B: name field 0x20 B (preserved verbatim), offset u32, size u32
data          member payloads, in table order and contiguous in every archive inspected
```

Commands:

```
python public_tools/fpk_repack.py --archive extract/files/d145.e --verify
python public_tools/fpk_repack.py --archive <fpk> --replace --member 0 --bytes new.bin --out out.fpk
```

Measured results on two real archives:

| archive | members | round-trip hash | verdict |
| --- | --- | --- | --- |
| `extract/files/d145.e` | 1 (`demo145.e…`, stored size 3,383, `ASH\0` payload) | `6fd025f2…bb37f1d` → identical | **PASS** |
| `extract/files/k01e010.m` | 21 (raw NSBMD members) | `d8ffe6c4…f80cc4d` → identical | **PASS** |

Replacements, both modes tested:

* **same size** (`k01e010.m` member 2, one byte flipped): the archive grows no bytes, the table is
  untouched, and a full byte diff against the input shows **exactly one differing byte**, at
  `0xC040`, inside that member's `0xBFDC..0xC45B` range.
* **different size** (`d145.e` member 0, 3,383 → 3,399 bytes): rebuilt archive, header and name field
  preserved, the member's table entry updated (`size 3383 → 3399`), payload preserved plus the 16
  appended bytes, archive `3,432 → 3,447` bytes.

Limitation that matters: the tool edits **stored** bytes. It does not decompress or recompress the
`ASH\0` container that script archives use, so a *decoded* edit cannot be put back yet (see the ASH
section below).

## ASH codec — header measured, token layer blocked

`public_tools/ash_codec.py` documents and parses the container header; the token codec is not
implemented, and the tool refuses to decode rather than guess.

Measured header (identical structure in `d145.e`, `d000.e`, `d004.e`):

```
0x00  41 53 48 00        magic "ASH\0"
0x04  e8 39 00 00        decoded size u32 LE (d145: 14,824 - matches the inventory's 4,100 + 10,724)
0x08  64 00 00 00        constant 100 in every archive inspected
0x0c  58 02 13 00        archive-specific word (0x00130258 / 0x00100515 / 0x001126d8)
0x10  0a 53 43 52 00 ff 09 00 ...   identical across all three archives; literal "SCR\0" sits at
                                    stored offset 0x11
```

The identical stream prefix across different scripts proves the codec is deterministic on identical
input prefixes (an LZ/RLE family), not a content-dependent tree. The token layer is still unknown:
brute force excluded every combination of flag-byte bit order and polarity, nibble/byte/high-bit
16-bit match tokens, literal-run control bytes with 1- and 2-byte distances, and 3-byte match tokens,
over stored offsets 8/12/16/17/20/21/100 - none produced 14,824 bytes starting with `SCR\0`. The
remaining plausible family is a Huffman/bit-plane stage (the constant `0x64` = 100 could be a tree
size), which cannot be implemented without a reference decode to validate against.

**Missing evidence:** one known-good decoded member (or the pinned reader's source) as a validation
oracle. The private inventory holds decoded hashes but not the bytes, and an unvalidated decoder is
how archives get corrupted.

```
python public_tools/ash_codec.py --info extract/files/d145.e      # header fields, exit 0
python public_tools/fpk_repack.py --archive extract/files/d145.e --decode-member 0 --out dec.bin
                                                                 # refuses with the reason, exit 1
```

`fpk_repack.py` now has `--decode-member` / `--encode-member` wired to this codec, so the moment the
token layer is validated the whole chain (decode -> edit -> encode -> repack) works with no further
plumbing.

## Half 2 — text payload: FAIL (with the exact missing evidence)

The text VM is documented in `docs/scripts/vm.md`: matched handlers write into a block at
`native_data_020FAE64`/`native_data_020FB264`, with the cursor at `+0x80`, and a matched walker
consumes the stream. What produced the characters is *not* matched, and the ledger says so:

| address | size | state | role |
| --- | --- | --- | --- |
| `0x02047B90` | 108 B | matched | text-family handler (writes a run) |
| `0x02047BFC` | 108 B | matched | alt-family handler |
| `0x02047AC0` | 208 B | matched | block walker / terminator handling |
| **`0x02047D50`** | **208 B** | **unmatched** | **string builder for the text family** |
| **`0x02047C68`** | **216 B** | **unmatched** | **string builder for the alt family** |
| **`0x02046E68`** | **52 B** | **unmatched** | **per-command length used by the walker** |

So the chain is broken at the exact point where characters appear: the two builders that hand a
produced string to the handlers are unmatched, and the length function that walks the stream is
unmatched too.

Two further facts rule out a shortcut:

* The block the handlers write into (`0x020FAE64`, `0x020FB264`) sits **above the end of the main
  image (`0x020E3300`) and below the overlay base (`0x021D7240`)** — the same uncovered gap that
  holds `species_roster`. No captured module image contains it, and `public/accepted-data.json`
  has no record for that range, so it is runtime BSS, not a ROM table.
* The script archives store their members inside an `ASH\0` container (see the `d145.e` row above),
  and the public tree has no ASH codec. A decoded edit therefore cannot be re-inserted even with
  half 1 working.

**Precise missing evidence:** the bodies of `0x02047D50` and `0x02047C68` (what a text handler
actually emits, and from which resource or table it reads), plus `0x02046E68` for the stream walk.
Without at least the two builders, no matched code connects a decoded `text_target_*` opcode to a
character in the ROM.

## What a romhacker can do today

1. Decode a script window: `python public_tools/scr_disasm.py --root <private> --image … --offset … --length …`.
2. Edit an opcode in that listing — changing both the byte column and the mnemonic, because the
   assembler refuses inconsistent listings — and reassemble with `public_tools/scr_asm.py`.
3. Repack a stored member with `public_tools/fpk_repack.py` (same-size in place, or rebuilt for a
   different size).
4. Verify every step: `scr_asm --roundtrip` shows the edit landing at exactly one offset, and
   `fpk_repack --verify` proves an unmodified archive round-trips byte for byte.

## What is still out of reach

* **Changing displayed text.** The string builders are unmatched and the text block is runtime BSS
  in an uncovered gap.
* **Re-inserting a decoded edit.** Script members are `ASH\0`-compressed; the header is measured but
  the token layer is blocked (see the ASH section), so no compressor exists yet.
* **Patching tables inside the ARM9 image.** The image is stored compressed, so the patch lane
  (`ops/mod_patch.py`) cannot reach table bytes; that needs the rebuild lane.

## Honest step list to close the gap

1. Match `0x02047D50` and `0x02047C68` (208 + 216 B) and confirm which resource or table they read.
2. If they read a table, locate that table in a captured image or in NitroFS, and add it to
   `docs/data/index.json` with a proven layout.
3. Validate an ASH decoder against one known-good decoded member, then implement compression; the
   header parser and the repack wiring already exist.
4. Only then: decode → change text → reassemble → repack → verify, which would turn this lens from
   PARTIAL to PASS.
