# aggregate-copy shape scan: the chunking class, enumerated from the image

Round 6 closed a seven-row aggregate-copy/chunking class by scanning the *image*
instead of a parked failure table. That class had never been enumerated, and the
row count was an artefact of the triage, not of the binary. This pass enumerates
it: every unmatched ledger row in every module is decoded from its measured bytes
and scored for the shapes a C compiler does not emit for a block copy. Sixty-three
rows (27,768 bytes) are reconstructed in the repository's verified-assembly form,
one address-named `.c` translation unit per function, each byte- and
relocation-exact with one mutated-instruction negative control per row.

## The class is twenty times larger than seven rows

| population | rows | bytes |
| --- | --- | --- |
| unmatched ledger rows scanned | 3,079 | - |
| rows carrying a non-frame block-transfer shape | 365 | 118,042 |
| the copy triage pool (predicated block, writeback run, or word run) | 145 | 75,974 |
| of those, already defined by a round-5 or round-6 lane | 18 | - |
| genuinely unclaimed candidates | 127 | 74,982 |
| shipped here (clear, `arm`, ≤ 1200 B) | **63** | **27,768** |

The seven round-6 rows are all rediscovered by the scan (`0x02001950`,
`0x0200197c`, `0x02005994`, `0x02029e90`, `0x021e4824`, `0x021e6040`,
`0x021e6158`), together with eleven round-5 rows in the same `memcpy` family
(`0x02000ce8`, `0x020010b8`, `0x020010e0`, `0x02008ca4`, `0x02008cdc`,
`0x02008cf0`, `0x02008d0c`, `0x02008d28`, `0x02008d4c`). Rediscovery is the
calibration: the screen finds the class that rounds 5 and 6 shipped, and 127 more
rows behind it.

The residual is real and is stated rather than implied: the Thumb half of the
class (`ov006`, 258 candidate rows) needs a `-thumb` lane, rows above 1200 bytes
were not attempted in this pass, and one picked row (`main:0x02025578`) contains a
jump-table word inside its measured extent that the pinned objdump leaves as
`<unknown>`, so it needs a hand decode.

## How the rows were found

`ops/scan_chunk_shapes.py` decodes every ledger row whose `functionMatched` flag
is false, in the row's own mode, and counts three shapes:

* a multi-register block transfer off a base **other than `sp`** with writeback
  (`ldm rN!` / `stm rN!`), because `stmdb sp!`/`ldmia sp!` frames are not a copy;
* a **predicated** multi-register transfer (`ldmneia`, `stmltia`, ...), which no C
  expression produces on this target;
* a run of at least four adjacent word `str`/`ldr` off one base with a `+4` stride,
  which is what an unrolled copy looks like when C emits a loop.

| module | unmatched rows | shape candidates | pool rows | shipped rows | shipped bytes |
| --- | --- | --- | --- | --- | --- |
| main | 976 | 50 | 42 | 13 | 6,252 |
| ov000 | 707 | 40 | 40 | 33 | 13,964 |
| ov001 | 758 | 11 | 11 | 11 | 4,204 |
| ov002 | 4 | 0 | 0 | 0 | 0 |
| ov003 | 17 | 1 | 1 | 1 | 756 |
| ov004 | 20 | 0 | 0 | 0 | 0 |
| ov005 | 89 | 4 | 4 | 3 | 1,524 |
| ov006 | 500 | 258 | 46 | 2 | 1,068 |
| ov007 | 0 | 0 | 0 | 0 | 0 |
| itcm | 8 | 1 | 1 | 0 | 0 |
| dtcm / arm7-* / utility-* | 0 | 0 | 0 | 0 | 0 |
| **total** | **3,079** | **365** | **145** | **63** | **27,768** |

The pool is ranked by shape count, then by size, exactly as round 6 triaged. All
clear `arm` rows up to 1200 bytes were attempted: 64 rows, of which 63 transcribed
exactly. The `itcm` row (8,920 B) is a whole-module function, not a copy.

## C was attempted first, per row

Each shipped row was compiled as C before it was transcribed. Three plausible
bodies per row were tried with the row's rule: a word copy loop, a block-struct
copy loop sized to the row's register list, and a guarded `*out = *in` struct copy
for the predicated rows. 189 compilations, **0 matches**. The closest body
(`ov005:0x021df4c4`, 36 B) still differs in 30 bytes; the median row differs in
over 97% of its bytes, and no row came within one instruction.

That is the expected result for this class and not a claim about C in general: the
image keeps a *rotated* loop with the test at the top and the copy predicated on
the result (`cmp; ldmlt; stmlt; blt`), keeps 8-register block moves where mwcc
schedules a shorter pair, and uses predicated block transfers that the compiler
folds into branches. Rows whose C form did match would have shipped as C; none did.

| shape | rows | bytes |
| --- | --- | --- |
| chunk loop (writeback load/store pair) | 27 | 10,516 |
| predicated block copy | 29 | 14,404 |
| block fill (writeback stores only) | 7 | 2,848 |

## Method

1. **Candidate screen, source first.** `ops/unclaimed.py --check-addresses` was run
   against a pristine `origin/main` (`ec661f64`) `src/` tree: **0 of 63** shipped
   addresses were already defined. Eighteen of the 145 pool rows were blocked this
   way — the seven round-6 rows and eleven round-5 rows — and were dropped before
   any drafting.
2. **Decode from the image.** `ops/transcribe_chunk.py` reads the row's measured
   extent, decodes it from the module image, reads every literal-pool slot out of
   the image, and resolves every branch target against the image. A pool word that
   lands inside the module image is a symbol (`native_data_<addr>`,
   `native_fn_<addr>`, `+1` for a Thumb code pointer); a magic constant such as
   `0x88888889` stays the numeric literal it is. Two slots holding the same value
   get distinct symbols (`native_data2_<addr>`) because the assembler would
   otherwise emit one slot.
3. **C attempt per row, then transcribe.** `ops/probe_c.py` compiles a candidate
   body and diffs the whole extent after relocation patching; the three bodies per
   row are recorded in the row table as "closest C body (bytes off)".
4. **Gate.** `ops/verify_asm_chunk_scan.py` compiles every file through its resolved
   rule, patches relocations the way `whole_image_link` does, compares every byte,
   checks every `R_ARM_ABS32` image word against the object symbol plus addend, and
   runs one mutated-instruction negative control per row.

## Spelling rules this pass added

Round 6's rules all held (standalone shift is `mov`; condition before width;
`push`/`pop` are `stmdb sp!`/`ldmia sp!`; a duplicated pool value needs an alias).
This population needed four more, each found by a compile error and each purely
lexical — no instruction was edited after the first transcription:

* a **conditional** block transfer needs the addressing mode after the condition,
  `ldmneia`; the disassembler's `ldmiane` is rejected, and the condition cannot be
  dropped from a conditional `pop` either: `pople` becomes `ldmleia sp!`, not
  `ldmia sp!` or `ldmiale sp!`;
* a conditional `push` is `stm<cond>db sp!`;
* a standalone shift that sets the flags is still a `mov`: `lsrs r0, r0, #0x1c`
  must be written `movs r0, r0, lsr #0x1c`;
* a conditional literal load keeps its condition on the `ldr rN, =symbol` form
  (`ldrmi r0, =native_data_...`), which is easy to lose when rewriting a
  `ldr r0, [pc, #n]` into a pool expression.

## Verification

```
python ops/verify_asm_chunk_scan.py            # 63 rows, 27768 bytes, 0 failures
python ops/verify_asm_chunk_scan.py --record   # refresh the pinned fixture
python ops/scan_chunk_shapes.py                # ranked shape table per module
python public_tools/source_units.py --root . --check   # unresolved: 0
python ops/unclaimed.py --root <pristine origin/main src/> --check-addresses \
    --address-file work/asm-chunk-scan/shipped.txt     # 63 addresses, 0 defined
```

`ops/asm_chunk_scan_expectations.json` pins, per row, the relocation table, the
image pool word behind every `R_ARM_ABS32` slot and the negative-control diff. The
lane resolves through six new rules under
`src/verified_assembly/20261112_asm_chunk_scan/{main,ov000,ov001,ov003,ov005,ov006}/**`,
all `p003` on `89b2fc16` (mwccarm 2.0/sp1p5). The `p001` profile the neighbouring
`20261111_asm_sweep1` lane uses produces identical bytes for these bodies — the
flag difference (`-opt speed`) does not reach an `asm` block — so the two lanes
differ only in the profile they name.

## Source-form rules these rows keep

1. **An `asm` function body is the reconstruction form for a row that resists C.**
   The build compiles it through the normal C rule; no new build path exists.
2. **A pool word is a relocation, not a constant.** `ldr rN, =native_data_<addr>`
   emits `R_ARM_ABS32`; the verifier proves the image word equals the symbol
   address plus addend. A pool word that is not an address is written as the
   numeric literal, so the object carries the measured word with no relocation.
3. **A call is a named symbol, never a raw offset.** `bl native_fn_<addr>` pins the
   callee by an address-bearing name.
4. **One negative control per row.** The first mutable instruction is changed (a
   register substitution, always encodable) and the control must differ from the
   image.
5. **One address-named file per function.**

## Rows

| address | module | bytes | shape | relocs | pinned pool words | closest C body (bytes off) |
| --- | --- | --- | --- | --- | --- | --- |
| `0x0204ce0c` | main | 508 | block fill | 31 | 0 | 503 |
| `0x0204d258` | main | 500 | block fill | 31 | 0 | 495 |
| `0x0205c49c` | main | 380 | chunk loop | 13 | 2 | 371 |
| `0x0206f7f8` | main | 832 | chunk loop | 30 | 2 | 828 |
| `0x02071748` | main | 992 | chunk loop | 33 | 3 | 985 |
| `0x0208423c` | main | 224 | chunk loop | 1 | 0 | 213 |
| `0x020bee08` | main | 320 | predicated block copy | 14 | 0 | 308 |
| `0x020bf148` | main | 208 | chunk loop | 2 | 0 | 201 |
| `0x020cb100` | main | 460 | chunk loop | 12 | 2 | 451 |
| `0x020d0ca8` | main | 408 | chunk loop | 12 | 2 | 398 |
| `0x020d19d4` | main | 552 | block fill | 16 | 2 | 542 |
| `0x020d1cf8` | main | 540 | chunk loop | 2 | 1 | 528 |
| `0x020d28cc` | main | 328 | predicated block copy | 4 | 0 | 314 |
| `0x021dd1e4` | ov000 | 192 | predicated block copy | 0 | 0 | 188 |
| `0x021dd2a4` | ov000 | 412 | predicated block copy | 2 | 0 | 402 |
| `0x021df950` | ov000 | 268 | chunk loop | 5 | 0 | 257 |
| `0x021e0498` | ov000 | 444 | chunk loop | 1 | 0 | 440 |
| `0x021e4388` | ov000 | 288 | chunk loop | 4 | 1 | 279 |
| `0x021e44a8` | ov000 | 272 | chunk loop | 4 | 1 | 262 |
| `0x021e45b8` | ov000 | 308 | chunk loop | 3 | 1 | 299 |
| `0x021e48dc` | ov000 | 364 | chunk loop | 4 | 1 | 355 |
| `0x021e4a48` | ov000 | 388 | chunk loop | 4 | 1 | 376 |
| `0x021e4bcc` | ov000 | 312 | chunk loop | 4 | 1 | 302 |
| `0x021e805c` | ov000 | 456 | predicated block copy | 18 | 0 | 446 |
| `0x021e8f28` | ov000 | 820 | predicated block copy | 24 | 0 | 809 |
| `0x021e925c` | ov000 | 1076 | predicated block copy | 30 | 0 | 1069 |
| `0x021e9794` | ov000 | 780 | predicated block copy | 14 | 0 | 768 |
| `0x021e9aa0` | ov000 | 800 | predicated block copy | 15 | 0 | 790 |
| `0x021ee0a4` | ov000 | 196 | block fill | 1 | 0 | 188 |
| `0x021f368c` | ov000 | 108 | predicated block copy | 2 | 0 | 99 |
| `0x021fae3c` | ov000 | 452 | block fill | 9 | 0 | 445 |
| `0x021fb250` | ov000 | 192 | block fill | 6 | 0 | 179 |
| `0x021fb7e8` | ov000 | 192 | predicated block copy | 6 | 0 | 188 |
| `0x021fdba0` | ov000 | 448 | block fill | 3 | 1 | 440 |
| `0x0220325c` | ov000 | 140 | predicated block copy | 2 | 0 | 129 |
| `0x022082f4` | ov000 | 836 | predicated block copy | 17 | 0 | 827 |
| `0x0220b94c` | ov000 | 220 | predicated block copy | 3 | 0 | 213 |
| `0x0220eb58` | ov000 | 580 | predicated block copy | 13 | 0 | 566 |
| `0x0220f858` | ov000 | 860 | predicated block copy | 36 | 0 | 842 |
| `0x02210a64` | ov000 | 268 | predicated block copy | 5 | 1 | 261 |
| `0x02212548` | ov000 | 420 | chunk loop | 5 | 0 | 411 |
| `0x02219728` | ov000 | 440 | predicated block copy | 19 | 0 | 433 |
| `0x0221fbb8` | ov000 | 180 | chunk loop | 7 | 0 | 174 |
| `0x0221fc6c` | ov000 | 116 | chunk loop | 3 | 0 | 110 |
| `0x0221fce0` | ov000 | 624 | chunk loop | 19 | 0 | 618 |
| `0x0221ff50` | ov000 | 512 | chunk loop | 10 | 0 | 507 |
| `0x021d80c0` | ov001 | 924 | predicated block copy | 14 | 0 | 918 |
| `0x021ee91c` | ov001 | 224 | chunk loop | 4 | 1 | 211 |
| `0x021ef224` | ov001 | 372 | predicated block copy | 12 | 0 | 353 |
| `0x021f1798` | ov001 | 108 | predicated block copy | 6 | 0 | 99 |
| `0x021f69a0` | ov001 | 844 | predicated block copy | 22 | 0 | 834 |
| `0x021f9588` | ov001 | 128 | chunk loop | 4 | 2 | 119 |
| `0x021fafec` | ov001 | 496 | chunk loop | 13 | 2 | 486 |
| `0x021ff2a8` | ov001 | 168 | chunk loop | 5 | 2 | 156 |
| `0x02203418` | ov001 | 68 | predicated block copy | 3 | 0 | 55 |
| `0x022061f4` | ov001 | 668 | predicated block copy | 22 | 0 | 652 |
| `0x0221e87c` | ov001 | 204 | chunk loop | 4 | 1 | 195 |
| `0x021dd300` | ov003 | 756 | chunk loop | 40 | 1 | 747 |
| `0x021db5d0` | ov005 | 296 | predicated block copy | 4 | 0 | 284 |
| `0x021df4c4` | ov005 | 36 | predicated block copy | 2 | 0 | 30 |
| `0x021e55e4` | ov005 | 1192 | predicated block copy | 37 | 5 | 1189 |
| `0x0220692c` | ov006 | 504 | predicated block copy | 13 | 1 | 497 |
| `0x0220728c` | ov006 | 564 | predicated block copy | 21 | 0 | 554 |

## Unknowns

Byte identity establishes the code, not the meaning. Each file states its own
unknowns; the recurring ones are the block and field roles behind the
`native_data_` targets, the record layouts and strides (0x34, 0x36, 0xc4, 0x140),
the callee contracts of the `native_fn_` targets, and which producer allocates the
destination blocks the copy loops fill. The numeric constants now kept as literals
(0x88888889, 0x66666667, 0x2aaaaaab, 0x38e38e39, 0x51eb851f, 0x0b60b60b) are the
usual reciprocal-multiply magic for division by 3, 5, 7, 10, 100 and friends; that
identifies the arithmetic, not the field it scales.
