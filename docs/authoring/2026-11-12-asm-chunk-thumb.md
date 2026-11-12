# the Thumb half of the aggregate-copy class, enumerated and opened

Round 7 enumerated the aggregate-copy/chunking class from the image and shipped
the ARM half: 63 rows, 27,768 bytes. Its own residual named the other half —
"`ov006`, 258 candidate rows needs a `-thumb` lane" — and left it untouched. This
pass closes that half: the Thumb pool is enumerated per module, the scanner and
transcriber now decode Thumb in its own dialect, and 60 rows (6,278 bytes) are
reconstructed in the verified-assembly form, one address-named `.c` translation
unit per function, each byte- and relocation-exact with one mutated-instruction
negative control per row.

## The Thumb pool, enumerated

`ops/scan_chunk_shapes.py --thumb` decodes every unmatched Thumb ledger row in the
row's own mode. A Thumb scan row carries at least one copy shape: a 16-bit
`ldm`/`stm` register-list transfer (the Thumb form of a writeback block move) or a
word `ldr`/`str` run. The triage pool is the round-7 definition applied to Thumb:
a predicated block transfer (none exist in Thumb-1), two or more writeback blocks,
or a word run. `push`/`pop` are decoded but not scored: they are the
`stmdb sp!`/`ldmia sp!` frame forms, and a frame is not a copy.

| module | unmatched Thumb rows | shape candidates | candidate bytes | pool rows | pool bytes | shipped rows | shipped bytes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| main | 201 | 19 | 20,182 | 11 | 13,978 | 5 | 698 |
| ov006 | 375 | 255 | 46,420 | 43 | 10,556 | 55 | 5,580 |
| **total** | **576** | **274** | **66,602** | **54** | **24,534** | **60** | **6,278** |

The Thumb half is larger than the ARM half in row count (274 shape rows against
365 for every ARM family) but much smaller per row: the median pool row is 200
bytes, the median shipped row is 52 bytes, and the largest shipped row is 604
bytes. The shipped 60 are 32 of the 54
pool rows (the clear, transcribable ones) plus the 28 smallest shape rows with one
writeback block, taken to carry the lane past the round's 40-row floor without
pretending the remaining 220 shape rows were attempted.

Twenty-two pool rows are refused with a reason, not silently skipped: 12 hold a
duplicated literal constant the assembler would fold into one slot, 9 contain a
pc-relative jump table inside the measured extent (the disassembler sees data as
instructions), and 3 load a literal slot outside the measured extent; two rows
carry two of those reasons. All 32 accepted pool rows compiled byte-exact.

## C was attempted first, per row

Each of the 60 shipped rows was compiled as C before it was transcribed, with
three plausible bodies and the row's Thumb rule:

1. a word copy loop (`do { *dst++ = *src++; } while (--count);`);
2. a block-struct copy whose struct is sized to the widest measured register list
   in the row (`*dst = *src;`);
3. a guarded copy loop (`if (count > 0) { ... }`).

180 compilations, **0 matches**. The closest body is 8 bytes off (ov006
`0x022010f8`, 56 B); the median row is 14 bytes off and the mean is 22.6% of the
row's bytes. That is much closer than the ARM half's median (over 97% off)
because these rows are small and the generic copy loop shares their
prologue/epilogue; no row came within one instruction, so every shipped row is
assembly. The exact per-row closest-C result is the last column of the row table.

## Method

1. **Scan.** `ops/scan_chunk_shapes.py --thumb --top 0` enumerates the pool and
   writes the per-row shape counts (`work/asm-chunk-thumb/thumb-scan.json` is this
   round's working copy). The ARM path and its round-7 totals are unchanged; the
   all-mode run still reports 145 pool rows / 75,974 bytes.
2. **Duplicate screen, source first.** `ops/unclaimed.py --check-addresses` ran
   against a pristine `origin/main` (`c9e7dfed`) `src/` tree: **0 of 60** shipped
   addresses were already defined. Mentions (callers, prototypes, comments) do
   not block a row.
3. **C attempt per row.** Three bodies per row through `ops/probe_c.py`; the row's
   ledger mode adds `-thumb`, and the patcher decodes the Thumb branch pair.
4. **Decode from the image.** `ops/transcribe_chunk.py` reads the row's measured
   extent, decodes it from the module image, reads every literal-pool slot out of
   the image and resolves every branch target against the image. A pool word that
   lands inside the module image is a symbol (`native_data_<addr>`,
   `native_fn_<addr>`, `+1` for a Thumb code pointer); a duplicated address-like
   word outside the image is named as the data pointer it is so the two slots stay
   two; a magic constant stays numeric. A literal slot outside the measured extent
   is refused, never guessed.
5. **Gate.** `ops/verify_asm_chunk_scan.py --lane
   src/verified_assembly/20261112_asm_chunk_thumb --fixture
   ops/asm_chunk_thumb_expectations.json` compiles every file through its resolved
   `mode: thumb` rule, patches relocations the way `whole_image_link` does,
   compares every byte, checks every `R_ARM_ABS32` image word against the object
   symbol plus addend, and runs one mutated-instruction negative control per row.

## Thumb specifics this pass had to learn

mwcc's Thumb assembler is a different dialect from its ARM assembler. Each rule
below was found by a compile error or a byte diff on a *sample*, fixed once in the
tool, and then held for every row — no instruction was edited after a row's first
transcription.

* **The `s` suffix is rejected.** `movs`, `adds`, `subs`, `lsls`, `asrs`, `ands`,
  `orrs`, `eors` are written `mov`, `add`, `sub`, `lsl`, `asr`, `and`, `orr`,
  `eor`; the 16-bit encoding still sets the flags. `bls`/`bcs` are branches, not a
  flag-setting `bl`, so the rewrite is an explicit mnemonic set.
* **`movs rX, rX` is not `mov rX, rX`.** LLVM prints the zero-shift encoding
  `0x00xx` as `movs rX, rX`; `mov rX, rX` assembles to `adds rX, rX, #0`
  (`0x1cxx`). The transcriber emits `lsl rX, rX, #0`.
* **`muls`/`rsbs` have Thumb operand counts.** `muls rD, rM, rD` is the
  two-operand `mul rD, rM`; `rsbs rD, rM, #0` is `neg rD, rM`.
* **`push`/`pop` are 16-bit instructions.** `stmdb sp!` / `ldmia sp!` do not
  exist in Thumb and are rejected; the ARM rewrite is not applied. `push
  {r4-r7, lr}` and `pop {r4-r7, pc}` assemble directly.
* **A Thumb block transfer always writes back and always names `ia`.** LLVM
  prints the 16-bit form as `ldm r3!, {r0, r1}` — and drops the `!` when the base
  is also in the list. mwcc wants `ldmia r3!, {...}`: `ldm` without `ia` is
  rejected, and omitting `!` when the base is in the list is a syntax error.
* **A bare `ldr rX, [rY]` directly after the `ldr rX, =symbol` pseudo-op is
  mis-assembled.** mwcc consumes the base register as an expression and encodes a
  non-zero offset. Writing the explicit zero offset (`ldr rX, [rY, #0]`) is the
  same encoding and is stable; every bare load/store in the transcriber is
  canonicalised this way.
* **Duplicate literal constants are deduplicated by value.** Two pool slots that
  hold the same magic constant compile to one slot, four bytes short. Distinct
  symbols keep both slots; an address-like duplicate outside the module image is
  named `native_data_<addr>`/`native_data2_<addr>`, and a duplicated non-address
  constant is refused rather than silently collapsed.
* **A Thumb function-pointer literal carries `+1`.** The image word is the odd
  function address; the source names `native_fn_<addr>+1`, so the relocation
  addend is 1 and the verifier's image-word check (`target + addend`) holds. 21 of
  the 60 rows carry one of these (28 relocations).

Two tooling holes were also Thumb-only:

* the scanner's 32-bit-instruction test was wrong for Thumb-1: `BL` starts at
  `0xF000` and the old `0xE800` test skipped the wrong halfword. The decoder now
  consumes `0xF000`-prefixed `BL`/`BLX` as one 4-byte instruction, and a run's
  adjacency stride is 2 bytes in Thumb, not 4;
* `R_ARM_THM_XPC22` (type 16), the BLX-to-ARM form mwcc emits for an interworking
  call outside the translation unit, was not handled by the relocation patcher.
  It is the same two-halfword immediate as `R_ARM_THM_CALL` (10) and
  `R_ARM_THM_JUMP24` (30); the measured site decides `BL` vs `BLX`, and
  `ops/thumb_branch.py` already applies the `Align(PC+4, 4)` base for `BLX`. 25
  of the 344 relocations are this kind.

## Verification

```
python ops/scan_chunk_shapes.py --thumb --top 0          # 274 candidates, 54 pool rows
python ops/verify_asm_chunk_scan.py \
    --lane src/verified_assembly/20261112_asm_chunk_thumb \
    --fixture ops/asm_chunk_thumb_expectations.json      # 60 rows, 6278 bytes, 0 failures
python ops/verify_asm_chunk_scan.py                     # round-7 ARM lane: 63 rows, 27768 B, 0 failures
python public_tools/source_units.py --root . --check    # unresolved: 0
python ops/unclaimed.py --root <pristine origin/main> --check-addresses \
    --address-file work/asm-chunk-thumb/shipped.txt      # 60 addresses, 0 defined
```

`ops/asm_chunk_thumb_expectations.json` pins, per row, the relocation table, the
image pool word behind every `R_ARM_ABS32` slot and the negative-control diff. The
lane resolves through two new rules under
`src/verified_assembly/20261112_asm_chunk_thumb/{main,ov006}/**`, both
`mode: thumb`, `p033` (the `-thumb` twin of the round-7 lane's `p003`) on
`89b2fc16` (mwccarm 2.0/sp1p5). All 60 rows compiled byte-exact on their first
attempt with the final transcriber; the per-row counts are 344 relocations
(211 `R_ARM_THM_CALL`, 108 `R_ARM_ABS32`, 25 `R_ARM_THM_XPC22`), 108 pinned pool
words, and 60 negative controls that each differ from the image in exactly one
byte (at offsets 0 to 5).

## Source-form rules these rows keep

1. **An `asm` function body is the reconstruction form for a row that resists C.**
   The build compiles it through the normal C rule; no new build path exists.
2. **A pool word is a relocation, not a constant.** A word that is an address is
   written as a symbol; a magic constant stays the numeric literal; a duplicated
   address-like word gets a distinct symbol so both measured slots survive.
3. **A call is a named symbol, never a raw offset.** `bl`/`blx native_fn_<addr>`
   pins the callee by an address-bearing name.
4. **One negative control per row.** The first mutable instruction is changed (a
   register substitution, always encodable) and the control must differ from the
   image.
5. **One address-named file per function.**

## Rows

| address | module | bytes | shape | relocs | pinned pool words | closest C body (bytes off) |
| --- | --- | --- | --- | --- | --- | --- |
| `0x02000e04` | main | 24 | block fill | 0 | 0 | 10 |
| `0x02008f3c` | main | 14 | block fill | 0 | 0 | 12 |
| `0x0209b368` | main | 208 | chunk loop | 6 | 2 | 10 |
| `0x020a51e4` | main | 284 | block fill | 3 | 2 | 14 |
| `0x020a9fc0` | main | 168 | block fill | 4 | 2 | 10 |
| `0x021ee6ac` | ov006 | 240 | block fill | 11 | 3 | 14 |
| `0x021eed5c` | ov006 | 232 | block fill | 11 | 3 | 14 |
| `0x021f1fa8` | ov006 | 232 | block fill | 10 | 4 | 14 |
| `0x021f2a4c` | ov006 | 40 | block fill | 1 | 0 | 10 |
| `0x021f2be0` | ov006 | 44 | block fill | 5 | 2 | 14 |
| `0x021f3494` | ov006 | 40 | block fill | 2 | 0 | 13 |
| `0x021f34bc` | ov006 | 40 | block fill | 2 | 0 | 14 |
| `0x021f3f74` | ov006 | 160 | block fill | 9 | 2 | 13 |
| `0x021f47f4` | ov006 | 52 | block fill | 3 | 1 | 10 |
| `0x021f53c8` | ov006 | 52 | block fill | 2 | 0 | 13 |
| `0x021f5444` | ov006 | 164 | chunk loop | 12 | 4 | 14 |
| `0x021f5d10` | ov006 | 112 | chunk loop | 14 | 3 | 14 |
| `0x021f5dcc` | ov006 | 40 | block fill | 2 | 1 | 14 |
| `0x021f7bf8` | ov006 | 44 | block fill | 5 | 1 | 14 |
| `0x021f7d48` | ov006 | 56 | block fill | 6 | 1 | 14 |
| `0x021f7ed8` | ov006 | 32 | block fill | 2 | 1 | 14 |
| `0x021f8b3c` | ov006 | 52 | block fill | 4 | 3 | 14 |
| `0x021f8f4c` | ov006 | 300 | block fill | 17 | 2 | 15 |
| `0x021f9314` | ov006 | 112 | block fill | 8 | 4 | 15 |
| `0x021f94ac` | ov006 | 248 | chunk loop | 18 | 5 | 11 |
| `0x021f9ac4` | ov006 | 56 | block fill | 1 | 1 | 12 |
| `0x021f9afc` | ov006 | 60 | block fill | 6 | 1 | 14 |
| `0x021f9b38` | ov006 | 112 | chunk loop | 8 | 4 | 14 |
| `0x021f9d84` | ov006 | 604 | block fill | 17 | 5 | 14 |
| `0x021fa7d0` | ov006 | 40 | block fill | 3 | 0 | 15 |
| `0x021fb7d0` | ov006 | 48 | block fill | 1 | 0 | 16 |
| `0x021fc1c8` | ov006 | 32 | block fill | 2 | 1 | 14 |
| `0x021fc484` | ov006 | 88 | block fill | 10 | 3 | 16 |
| `0x021fcb50` | ov006 | 192 | chunk loop | 23 | 5 | 14 |
| `0x021fd62c` | ov006 | 52 | block fill | 2 | 1 | 10 |
| `0x021fdbc8` | ov006 | 84 | chunk loop | 7 | 2 | 10 |
| `0x021fe200` | ov006 | 52 | block fill | 6 | 2 | 10 |
| `0x021fe4dc` | ov006 | 32 | block fill | 4 | 2 | 13 |
| `0x021ff6b4` | ov006 | 32 | block fill | 4 | 2 | 14 |
| `0x021ffd50` | ov006 | 132 | block fill | 7 | 2 | 14 |
| `0x021ffdf4` | ov006 | 52 | block fill | 5 | 2 | 10 |
| `0x02200344` | ov006 | 516 | block fill | 31 | 10 | 14 |
| `0x02200950` | ov006 | 36 | block fill | 2 | 1 | 14 |
| `0x02200a04` | ov006 | 120 | block fill | 9 | 3 | 14 |
| `0x02200a7c` | ov006 | 44 | block fill | 2 | 1 | 9 |
| `0x022010f8` | ov006 | 56 | block fill | 2 | 2 | 8 |
| `0x0220167c` | ov006 | 56 | block fill | 5 | 1 | 14 |
| `0x022022ac` | ov006 | 56 | block fill | 1 | 1 | 14 |
| `0x02202c1c` | ov006 | 64 | block fill | 5 | 2 | 14 |
| `0x02202d64` | ov006 | 92 | block fill | 2 | 0 | 16 |
| `0x02203058` | ov006 | 48 | block fill | 3 | 0 | 13 |
| `0x022033ec` | ov006 | 64 | block fill | 5 | 2 | 10 |
| `0x02203cfc` | ov006 | 152 | block fill | 0 | 0 | 13 |
| `0x02203eec` | ov006 | 48 | block fill | 0 | 0 | 14 |
| `0x02203f1c` | ov006 | 48 | block fill | 0 | 0 | 14 |
| `0x02204364` | ov006 | 36 | block fill | 4 | 2 | 14 |
| `0x022043a4` | ov006 | 60 | block fill | 1 | 1 | 16 |
| `0x02204874` | ov006 | 52 | block fill | 5 | 2 | 14 |
| `0x02204974` | ov006 | 24 | block fill | 1 | 1 | 11 |
| `0x02204994` | ov006 | 48 | block fill | 3 | 0 | 12 |

## Unknowns

Byte identity establishes the code, not the meaning. Each file states its own
unknowns. The recurring ones are the block and field roles behind the
`native_data_` targets, the record layouts and strides the copy loops touch, the
callee contracts of the `native_fn_` targets, and which producer allocates the
destination blocks. The numeric constants kept as literals (0x0221c134,
0x0221c1ac, 0x0221c15c, 0x00000808, 0x00001e5c, and the usual reciprocal
multipliers) identify addresses or arithmetic, not the field they scale.
