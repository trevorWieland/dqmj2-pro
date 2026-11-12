# main families: the guarded accessors and the SDK memory primitives

Twenty-five unmatched `main` rows are reconstructed in one lane directory,
**720 bytes total**, byte- and relocation-exact against `extract/arm9/arm9.bin`.
Thirteen of them are the two families this pass was opened for: the five guarded
field accessors at `0x02083da8`-`0x02084080` and the eight aggregate copy/fill
primitives at `0x02008c14`-`0x02008d4c`.

| family | rows | bytes | exact |
| --- | --- | --- | --- |
| A: guarded field accessors | 5 | 160 | 5 |
| B: SDK copy/fill primitives | 8 | 224 | 8 |
| B seam, adjacent (`0x02008ca4`) | 1 | 56 | 1 |
| fill: hardware/runtime leaves | 11 | 280 | 11 |
| **total** | **25** | **720** | **25** |

## The finding that decided both families: they are not C

Both families were carried as "C form unknown" in the pass-2 lane. They are not
C-form problems. The measured streams are the original SDK assembly, and the
repository already reconstructs that kind of row this way: the accepted
neighbours `0x02008c58` (`src/verified_assembly/20261102_mi_clear76`),
`0x02008d78` and `0x02008e0c` (`src/mechanics_save/saved_sdk_*_original.s`) are
hand-written assembly too, and they bracket the family-B range.

Evidence, in the order it was gathered:

1. **Family A.** The image pins the guard as a *predicated early return*
   (`tst r0, #0x1f` / `movne r0, #0` / `bxne lr`) and keeps the store
   unconditional on the fall-through path. Every C shape tried — plain early
   return, inverted `if/else` with distinct returns, a shared `goto fail` label,
   `s32 result = 0; ... result = 1; return result;`, a variable zero, a
   `switch`, a `do/while(0)`, a `while (cond) return 0;` loop, a volatile store,
   a volatile pointer local, a declaration after the guard, a statement
   expression, and a macro-wrapped guard — compiles to the folded form
   (`ldreq` / `streq` / `moveq` / `bx`), which is 28 bytes against the image's
   32. That is mwccarm's if-converter merging the two returns; it is not a
   source-form choice.
2. **Family A across the toolchain.** The naive form was compiled with every
   installed build (26 of them: every `1.2`, `2.0`, `dsi` and recovered year
   build) at every flag profile in `config/source_units.json` (73 profiles,
   including all the `-opt speed`, `-opt space`, `-O3` and `-O4` variants) —
   **not one** produces the 32-byte stream. The class is closed for this
   installed toolchain.
3. **Family B.** The aggregate rows are
   `ldm/stm` chunk sequences: `ldm r0!, {...}` / `stm r1!, {...}` in 12-byte
   chunks with `r2, r3, r12` as the move registers, unrolled, and a final chunk
   that reuses `r0` (`ldm r0, {r0, r2, r3, r12}`). C struct assignment:
   * a 16-byte struct copy gives `mov r3, r1; ldm r0, {r0, r1, r2}`);
   * a 32-byte copy gives `push {r3, lr}` plus two four-register moves;
   * a 48-byte copy is turned into a three-iteration counted loop with a frame;
   * a run of `*dst++ = *src++` statements is re-associated into a running
     pointer plus `add` offsets and grows to 56-72 bytes.
   None of them emits the three-register/writeback chunking, and none of them
   keeps the pointer arguments in `r0`/`r1`. The `r0` reuse in the final chunk
   of `0x02008d4c` exists precisely *because* the source pointer is dead there,
   which is an assembly-level allocation decision.
4. **Family B loops.** `0x02008c14`/`0x02008c28`/`0x02008c40` use
   `stmlt r1!, {r0}` / `ldmlt r0!, {r2}`: single-register block transfers taken
   under a predicate, with the test rotated in front of the body. The C fill
   loop compiles to `str r0, [r1], #4` with a `b` to a rotated test and is four
   bytes longer; no loop shape or declaration order changes that.

## What cracked them

Given (1)-(4), the reconstruction is transcription of the measured stream, in
the repository's existing form: a `.c` translation unit whose function is an
mwccarm `asm` function, so the build path, the source-unit rule and the ledger
naming rules are unchanged. `src/verified_assembly/**` already resolves to
`p001` on `2.0/sp1p5` (`89b2fc16`), which is what these rows are assembled with.

The five accessors need a literal-pool word, which is expressed as
`ldr r1, =native_data_<addr>` and therefore carries a real `R_ARM_ABS32`
relocation; the verifier checks the image word against the symbol address, so
the pool word is never hard-coded.

### Rows

| address | bytes | family | relocs | control diff |
| --- | --- | --- | --- | --- |
| `0x02083da8` | 32 | A | 1 (`.data @ 0x021c72a0`) | `[0]` |
| `0x02083dc8` | 32 | A | 1 (`.data @ 0x021c72a0`) | `[0]` |
| `0x02083de8` | 32 | A | 1 (`.data @ 0x021c72a0`) | `[0]` |
| `0x02084028` | 32 | A | 1 (`.data @ 0x021c9600`) | `[0]` |
| `0x02084080` | 32 | A | 1 (`.data @ 0x021c9600`) | `[0]` |
| `0x02008c14` | 20 | B | 0 | `[2]` |
| `0x02008c28` | 24 | B | 0 | `[2]` |
| `0x02008c40` | 24 | B | 0 | `[2]` |
| `0x02008cdc` | 20 | B | 0 | `[2]` |
| `0x02008cf0` | 28 | B | 0 | `[2]` |
| `0x02008d0c` | 28 | B | 0 | `[2]` |
| `0x02008d28` | 36 | B | 0 | `[2]` |
| `0x02008d4c` | 44 | B | 0 | `[2]` |
| `0x02008ca4` | 56 | B seam | 0 | `[0]` |
| `0x02000ce8` | 36 | fill | 0 | `[1]` |
| `0x020010b8` | 40 | fill | 0 | `[1]` |
| `0x020010e0` | 52 | fill | 0 | `[0]` |
| `0x02006018` | 12 | fill | 1 (callee `0x02005ff8`) | `[1]` |
| `0x02007850` | 20 | fill | 2 (callees) | `[0]` |
| `0x02007e98` | 16 | fill | 1 (callee `0x02007ea8`) | `[0]` |
| `0x02008064` | 12 | fill | 0 | `[2]` |
| `0x0200829c` | 8 | fill | 0 | `[0]` |
| `0x0200fb48` | 24 | fill | 1 (`.data @ 0x020e5444`) | `[1]` |
| `0x02029cc4` | 52 | fill | 2 (`.data @ 0x020edd0c`, `@ 0x04000350`) | `[1]` |
| `0x0208a690` | 8 | fill | 0 | `[0]` |

## First-try rate

Measured over the forms actually attempted before the family was understood:

| stage | forms attempted | rows landed on that stage |
| --- | --- | --- |
| family A C forms | 40 distinct C bodies (plus the 26-build x 73-profile sweep) | 0 |
| family B C forms | 20 distinct bodies (struct copy, chunk copy, post-increment, loop shapes) | 0 |
| family A/B transcription | 13 | **13 first-try** |
| fill rows | 11 | 9 first-try, 2 after a C near-miss |

Two fill rows have a measured C near-miss worth recording:

* `0x0200fb48` (spin until a status word leaves 1): the volatile-pointer C form
  is 24 bytes and matches except for the block base, which mwcc puts in `r1`
  where the image uses `ip` (differ at bytes 1 and 6).
* `0x02029cc4` (replace a five-bit field, mirror the word): the C form is 48
  bytes against 52 because mwcc schedules the two pool loads after the read.

## Source-form rules these rows keep

1. **An `asm` function body is the reconstruction form for an SDK row.** The
   build compiles it with the file's own rule; nothing special is needed.
2. **A pool word is a relocation, not a constant.** `ldr rN, =native_data_a`
   emits `R_ARM_ABS32`; the verifier proves the image word equals the symbol
   address.
3. **A call is a named symbol, never a raw offset.**
   `bl native_fn_02007ea8` pins the callee by address-bearing name.
4. **One negative control per row.** The first instruction of the body is
   mutated (constant xor, register step, or a dropped register), the control is
   compiled with the same rule, and its diff from the image must equal the
   pinned offset list in `ops/main_families_expectations.json`.

## Verification

```bash
python ops/verify_main_families.py            # 25 rows, 720 bytes, 0 failures
python ops/verify_main_families.py --record   # refresh the pinned fixture
```

Per row: the object's relocation table equals the pinned one; every `R_ARM_ABS32`
slot equals the object's relocation target; the whole measured extent is
byte-identical; and the mutated control compiles and differs at the pinned
offsets. The fixture also records the pool word each row loads, so a re-run
shows the data address behind every literal.

## Unknowns

Byte identity establishes the code, not the meaning. Open questions are stated
in each source file: the `0x021c72a0` / `0x021c9600` blocks behind the five
accessors and why a 32-byte-aligned value is required; the record layouts and
buffer roles of the eight copy primitives; which hardware windows
`0x02000ce8` / `0x020010b8` / `0x020010e0` program; what the field replaced by
`0x02029cc4` selects and what `0x04000350` is; which producer clears the status
word polled by `0x0200fb48`; and the caller contracts of the three call
trampolines.
