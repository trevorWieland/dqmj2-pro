# Three existing comparator sources with defined field extraction

This is a zero-coverage migration proposal for three already selected main ARM9 ARM functions. All historical primary files remain unchanged. The proposed sources are under `src/mechanics_save/20261031_lane_comparator_abi/` and genuinely compile/link to every original byte with the explicit pinned MW2.0-base settings in their reports.

| Entry | Measured bytes | Proposed source SHA-256 | Frozen historical primary |
| --- | ---: | --- | --- |
| `0x0207CB3C` | 176 | `ff529f42481807db77b2c9c51125c4f7b148e7029a88fdc6b727349301b8c0e8` | `src/runtime/runtime07/native_main_0207cb3c.c` |
| `0x0207CBEC` | 136 | `8405ce718015aa580da49c8b3b36499ba8506c1c8d2a63e60ce2060af0f65429` | `src/runtime/runtime10/native_main_0207cbec.c` |
| `0x0207CD04` | 148 | `177dcf35c8d0f57559e96d4145154986f7c456084ff29088eb7a10b511012c8b` | `src/runtime/runtime07/native_main_0207cd04.c` |

The total is 460 already counted native bytes, with zero additional executable or function credit. A preliminary 160-byte estimate for the third function was rejected by the builder's measured identity guard before real linking. The accepted candidate uses the configured range `0x0207CD04..0x0207CD98`, 148 bytes, and does not borrow the next 12 bytes. That failed boundary assumption is preserved separately.

Run `python match_mechanics_save_20261031_lane_comparator_abi.py`. Canonical report `evidence/matches/mechanics-save-20261031-lane-comparator-abi.json` is SHA-256 `7c2c20e21ef99b179d49aabdbe29129a6e2d54b55c5a981df926c50c13bca333`, identical for repository and parent-working-directory runs. Native vector digest is `f118f2e39f47e5b0330d253adf4aa9a439f814963c5c56e337d54303ba98eec1`. The command builds all preferred and wrong-source objects locally, validates current source/object/real-link/native identities, and creates all consumed reports. It introduces no generated-golden ordering prerequisite. Primary selection and all-module acceptance remain integrator-owned.

## Existing source issue and distinct native policies

All three historical sources mask descriptor halfword `+6` by left-shifting its promoted signed-int value, then casting to unsigned. A later cast does not prevent signed overflow during the shift. On the original 512-record descriptor payload, 480 such halfwords exceed the safe signed-shift range. `0x0207CB3C` also extracts descriptor halfword `+4` bits 4 through 7 with a promoted signed left shift; 508 original halfwords overflow that shift. Matching target bytes alone therefore did not prove a defined ordinary-C expression suitable for further reuse.

The proposed sources use ordinary unsigned-short bitfields for the measured four-bit and 13-bit fields. Their normal integer promotions keep the compared values representable, and the difference results fit signed 32 bits. The callback return type is explicitly signed; UID words remain unsigned and preserve all 32 bits. No original SDK field names, high-bit meanings, forced registers, volatile coloring, executable byte arrays, assembly, or opcode patches are added. These are qualified NDS memory/type views, not a completed shared-header or 64-bit address-mapping migration.

The three first-stage comparisons are different and are modeled independently:

- `0x0207CB3C` compares descriptor `+4` bits 4 through 7 in ascending order.
- `0x0207CBEC` compares raw record byte `+0x30` (decimal 48) in descending order. No level, ownership, or status meaning is assigned to that byte.
- `0x0207CD04` calls original `0x02044CDC`, comparing its descriptor `+4` bits 8 through 11 divided by three in ascending order. The selected dependency already has a proper bitfield implementation in `src/mechanics_save/library.c` and is reused unchanged.

All ties compare descriptor `+6` low 13 bits in descending order. Both zero UID words still return signed -1: the native right-zero check runs before the left-zero check. No total-order or reflexivity correction is inferred. Static caller `0x0207CA3C` selects these callbacks for modes 1, 2, and 4 and passes 100 four-byte words to native sort `0x0201D470`; ordinary enclosing scene reachability is not established.

## Independent returning execution

The fixture retains actual original UID lookup `0x02062A10`, descriptor addressing `0x020449D4`, the CD04 category helper, and the complete native sort. It uses zero providers. Every original descriptor, complete nibble ranges, low-13/high-three key boundaries, full raw byte-48 values, same-UID/same-pointer cases, and sentinel short circuits are checked. Record pools are deterministic disposable synthetic state; no save-bank validation or record-validity assertion follows.

| Callback | Direct pairs | Native-sort pairs | Actual top returns |
| --- | ---: | ---: | ---: |
| `0x0207CB3C` | 1,359 | 14 | 2,746 |
| `0x0207CBEC` | 2,127 | 14 | 4,282 |
| `0x0207CD04` | 1,359 | 14 | 2,746 |

The total is 4,887 pairs and 9,774 actual top-level returns, including 84 native-sort host returns. Separately observed native helper returns total 81,256 and nested comparator returns inside sort total 7,692. Both engines execute 18,686,540 instructions. Actual callback words are observed where original sort consumes them using signed comparisons. An independent per-policy multiset/key model verifies sorting without inventing stable ordering for ties.

The complete readonly record pool, descriptor payload, operand words and canaries, sort-array writes, ordered operand reads, every helper argument and returned word, registers/CPSR, stack hashes, restored SP, and bounded actual termination agree between original and complete C. Thirty-six separate null-pointer, missing-UID, negative-species, and beyond-backed-species stops are excluded, with no post-fault credit. Backing guards describe this fixture's supported domain and do not claim that the game validates malformed records.

Run `python evidence/application/save_core_comparator_abi_controls_20261031.py`. Its report SHA-256 is `e2622f5f8b49abcfeaad5631cc17bb84c58c8c683e644228bc2dc61a66af47c0`. Three complete wrong C functions retain the distinct first-stage policies but widen the key from 13 to 16 bits. They genuinely compile/link, and shorter bodies have strict fetch bounds preventing use of original trailing bytes. All 18 original and 18 wrong-source calls return. Nine independent signed-result expectations reject upper-bit inclusion; nine positive controls retain original results. No wrong-source or repeated accepted bytes receive coverage credit.

All original ROM/save hashes, historical primaries, previous accepted matches, baseline, and application files remain unchanged. The 40,560 semantically unknown save bytes remain preserved and unclassified. Full clean source/module/whole-ROM replay and audited preference replacement remain separate integrator gates.
