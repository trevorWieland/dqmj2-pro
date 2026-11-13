# Data layout and `.rodata` / `.data` ordering

Status: infrastructure, measurement and bounded proof added on branch `codex/data-layout`
(2026-11-12). The measured baseline is the real `public_tools/repo_build.py` compile and
compare of `main` at `c16723ed`:

| measure | value |
|---|---:|
| initialized code bytes matched | 1,765,974 / 2,129,010 |
| functions matched | 14,159 / 15,308 |
| initialized data bytes matched | 109,484 / 383,626 |
| compiled source units | 14,544 |

The task snapshot quoted 1,750,050 / 2,129,010 and 14,113 / 15,308; the tree advanced by
about 16 KiB of code and 46 functions during this work. The data figures are identical.

## Why a layout model is needed

A C compiler does not preserve source order in an object's initialized data. MWCC emits one
`.rodata` or `.data` section per alignment group and fills each group in an order of its own.
Two source files with the same literals can therefore produce different byte sequences. A
file's compiled data can only be reproduced by measuring the emitted permutation and
declaring the literals in the order that makes the compiler emit the original sequence.

This is distinct from content: the same blocks can be present in the wrong order. Without a
model, the only safe authoring style is one symbol per compile, which is what the accepted
data snapshot currently does for most units. That style is correct but does not scale to
files that naturally contain several strings or constants.

## Measurement

Method: every compiled source unit is parsed into its emitted data sections and object
symbols (`ops/data_layout.py`), each block is placed at its measured address (address-bearing
symbol name, accepted-data record, or a unique content search), the block bytes are compared
with the original module image after applying ABS32 relocations, and the file is classified:

* **exact** - every block matches at its measured address and the emitted order is the
  measured address order (contiguous or one block);
* **order** - every block matches, but the emitted sequence is a permutation of the measured
  sequence;
* **content** - at least one placed block's bytes differ;
* **unresolved** - a compiler-synthesized literal has no independent measured address
  (for example an inlined mask), so it cannot be placed or counted.

Main module (host ARM9, `0x02000000` base), baseline before the bounded application:

| class | files | bytes |
|---|---:|---:|
| exact | 369 | 6,011 |
| order | 1 | 20 |
| content | 0 | 0 |
| unresolved | 10 | 67 |

Main module after the bounded application on this branch:

| class | files | bytes |
|---|---:|---:|
| exact | 388 | 6,607 |
| order | 0 | 0 |
| content | 0 | 0 |
| unresolved | 10 | 67 |

The 19 new exact units are the 18 generated `src/main/data_layout` files (576 B) and the
reordered port file (20 B). The accepted subset is unchanged at 369 files / 6,011 B because
the bounded units are not registered in the accepted-data snapshot.

Overlay `ov001` (`0x021d7240` base):

| class | files | bytes |
|---|---:|---:|
| exact | 0 | 0 |
| order | 0 | 0 |
| content | 0 | 0 |
| unresolved | 0 | 0 |

`ov001` has 9,064 initialized data bytes in the original image and **no compiled C source
that defines data**. Its data gap is unauthored regions, not a source-order defect. Main has
62,224 initialized data bytes; 6,031 bytes (9.7%) are emitted by compiled source, and 20 of
those bytes are the only order-only case in the tree.

The one order case is `src/ports/20261102_anim_graph1004/driver.c`: five function-pointer
words are declared `608, 604, 600, 5f8, 5fc` but measured at `5f8, 5fc, 600, 604, 608`. The
compiler emits `5f8, 600, 604, 608, 5fc`, a permutation of the measured sequence. The source
was reordered to `604, 600, 5fc, 5f8, 608`; the object's `.data` now equals the measured
20-byte region and the object's `.text` sections hash identically before and after.

The accepted data snapshot contains 462 records, of which 450 are initialized records
(450 distinct sources, 109,484 bytes). Most are data-only generated assets; main accounts
for 25,890 matched data bytes and `ov001` for 0. The 369 exact files above are code files
whose local constants are already accepted one symbol at a time. Their data was already
counted; this measurement confirms that content is not the problem in accepted source and
isolates the remaining gap as unauthored data.

## The ordering rule

`ops/data_layout.py rule-check` compiles seven synthetic probes with the pinned compiler and
data profile. All seven agree with:

```
emission = reverse(declaration[:-1]) + [declaration[-1]]
```

Equivalently, for `n > 1`, the compiler emits declarations `n-2 ... 0` in reverse and
declaration `n-1` last; `n == 1` is unchanged. The inverse used to author a measured
sequence is:

```
declaration = reverse(emission[:-1]) + [emission[-1]]
```

Probe evidence (`n` = declaration count, all from `mwccarm 2.0/base`):

| n | emitted order (declaration indices) |
|---:|---|
| 2 | 0, 1 |
| 3 | 1, 0, 2 |
| 4 | 2, 1, 0, 3 |
| 5 | 3, 2, 1, 0, 4 |
| 6 | 4, 3, 2, 1, 0, 5 |
| 8 | 6, 5, 4, 3, 2, 1, 0, 7 |
| 12 | 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 11 |

The same rule holds for equal-sized arrays (six `const int[1]` declarations and six
same-size `const char[]` declarations both emit `5,4,3,2,1,0`-style order).

Hypotheses tested against the probes and the measured classes:

| hypothesis | verdict | evidence |
|---|---|---|
| source declaration order | rejected for `n >= 3` | probe `n=6` emits `4,3,2,1,0,5` |
| reverse declaration order | accepted with a tail exception | `reverse(decl[:-1]) + [decl[-1]]` in all seven probes |
| size-descending | rejected | equal-size probes still permute; six 4-byte words emit `4,3,2,1,0,5` |
| alignment-grouped | accepted for section partitioning, rejected for intra-group order | one section per alignment; within a homogeneous group the reverse rule applies |
| name or content hash | rejected | renaming or changing initializer values did not change the emitted index order |
| section-size ordering | accepted only across different-size array sections | `const char[]` sizes 4,6,6,7,7,7 emitted size-ascending |

The declared-order/reverse rule explains the entire measured order-only class (20 B / 20 B)
and the 576 bytes of bounded files authored here. Section grouping explains why a file with
mixed-size arrays cannot be ordered by declaration; that is recorded as a model break, not
as bytes explained.

### What else the compiler does

* **Alignment groups become separate sections.** MWCC writes one `.rodata`/`.data` section
  per alignment. The linker concatenates same-named sections in object order, so
  cross-section order is part of the layout.
* **Different-sized `const char[]` arrays get separate sections ordered by size, not by
  declaration.** A probe with sizes 4, 6, 6, 7, 7, 7 emitted sections in size-ascending
  order. This is the main falsifier for multi-string files: declaration order cannot
  reproduce an arbitrary address order across size classes.
* **Direct string literals** used in a function were emitted in declaration order in
  `.data` in the probe, but they carry no independent data symbol and bring `.text` with
  them, so they are not a data-only authoring mechanism.
* **Non-contiguous measured symbols cannot be one source file.** `src/arm7/20261101_wl_parameters220/ordinary_wireless.c`
  emits two tables contiguously, while the measured copies are 212 bytes apart
  (`0x27f72ec`, 32 B and `0x27f73c0`, 240 B). No declaration order fixes that; the file
  needs a linker placement or a filler region.
* **Compiler-synthesized constants are not addressable.** Inlined masks (`cmask0$50`,
  `fullbits$41`, `useAlternateEncoding$9`, `@24`) appear as local `.rodata` symbols but have
  no measured address of their own. Ten main files / 67 bytes remain in this class; they
  are not data-region candidates.

The rule therefore explains the complete order-only class in the measured tree (20 B /
20 B) and every homogeneous equal-size group tested. It does not explain, and cannot
explain, files whose measured symbols are non-contiguous or whose declarations cross size
classes. Those cases are reported as `breaks` by the tool instead of being guessed.

## Tool

`ops/data_layout.py` (Python standard library only) models the emitted layout, compares it
with the original image, and inverts the rule.

```powershell
# classify one compiled data unit against a measured region
python ops/data_layout.py compare --object unit.o --image extract/arm9/arm9.bin `
    --base 0x02000000 --start 0x020d90ac --end 0x020d90cc

# emit the declaration order that reproduces the measured sequence
python ops/data_layout.py order --object natural.o --image extract/arm9/arm9.bin `
    --base 0x02000000 --start 0x020d90ac --end 0x020d90cc

# gate a data source: object bytes, real MWLD placement, and unchanged .text
python ops/data_layout.py verify --object unit.o --image extract/arm9/arm9.bin `
    --base 0x02000000 --start 0x020d90ac --end 0x020d90cc `
    --linker tools/mwccarm/mwccarm/2.0/base/mwldarm.exe `
    --baseline-object baseline.o

# re-measure every compiled source file's emitted data blocks
python ops/data_layout.py measure --root . --modules main,ov001 `
    --json work/data-layout/measure.json

# verify the compiler rule itself (7 probes)
python ops/data_layout.py rule-check `
    --compiler tools/mwccarm/mwccarm/2.0/base/mwccarm.exe
```

`compare`/`order`/`verify` preserve duplicate section names (one per alignment group),
apply ABS32 relocations from the object, and report `classification`, `blocks`, `moves`,
`targetSequence`, `declarationOrder`/`declarationNames`, `model` and `breaks`. `verify`
links the object with the pinned `mwldarm` at the measured `ORIGIN`; a code-bearing unit
whose external symbols are unavailable is reported as `link.exact: null` rather than
silently passing, and the caller must use the `.text` baseline gate.

## Bounded application

Eighteen data files were generated from real measured main-module regions:

* `src/main/data_layout/words_020d90ac.c` through `words_020d90f0.c` (11 files, 352 B);
* `src/main/data_layout/words_020dcd30.c` through `words_020dcdb0.c` (5 files, 160 B);
* `src/main/data_layout/words_020d9014.c`, `words_020d9034.c` (2 files, 64 B).

Each file declares eight 4-byte constants. Natural address-order declarations emit the
sequence reversed except the last (the rule above), so each file declares them as
`6,5,4,3,2,1,0,7`; the object's `.rodata` is then byte-identical to the measured 32-byte
region. All eighteen pass `ops/data_layout.py verify` with both the object comparison and a
real `mwldarm` placement at the measured address.

The port reorder above (20 B) is the only real source reorder demanded by the measured
order-only class. Both changes are bounded: 596 bytes of initialized data across 19 units.

To prove the credit path rather than only the object path, the accepted-data snapshot was
temporarily extended with 19 records (the 18 files plus the driver's 20-byte `.data` span)
and the real project/report path was rerun:

| report | matched data | percent | complete units |
|---|---:|---:|---:|
| baseline | 109,484 | 28.539% | 14,609 |
| plus bounded records | 110,080 | 28.695% | 14,628 |

The snapshot was restored afterwards; registering the records is coordinator-owned and is
not part of this branch. The point of the delta is that the real `repo_build` project path
counts these bytes when the evidence is registered, not that a hand-edited snapshot is a
publication input.

## Reproduce

```powershell
# compile the complete tree with the pinned toolchain
python public_tools/repo_build.py --root . --private-root . --compile-only --jobs 8

# build the project and the real report
python public_tools/repo_build.py --root . --private-root . --project-only --jobs 8
tools/objdiff/3.8.3/objdiff-cli.exe report generate --project build/B2JJ-modified `
    -o build/B2JJ-modified/report.json

# the rule probes and the bounded units
python ops/data_layout.py rule-check --compiler tools/mwccarm/mwccarm/2.0/base/mwccarm.exe
python ops/data_layout.py measure --root . --modules main,ov001
```

## Limits

* The measurement uses the compiler objects of the last full compile. A source change must
  be followed by a fresh `repo_build --compile-only` before re-measuring.
* The tool places a block by its symbol name, a registered accepted-data address, or a
  unique content search, in that order. A block with none of those is `unresolved` and is
  not counted as exact.
* ABS32 words are resolved from the original image at the same site. Other relocation kinds
  are preserved but not synthesized; a data region containing them needs a real link test.
* The rule is a compiler-version rule. All probes here are `mwccarm 2.0/base`; a unit
  promoted to `1.2` or `2.0/sp1` must be re-probed with that compiler.
* The model is deliberately not extended to the size-sorted multi-array case: the tool
  reports a `break` instead of emitting an order that the compiler will not honour.
