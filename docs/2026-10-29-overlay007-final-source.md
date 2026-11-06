# Overlay 007 remaining source and linker metadata, 2026-10-29

This handoff reconstructs the last three configured ordinary ARM functions in overlay 007 as C: 021D7D7C/104B, 021D8AF8/200B and 021D9040/248B. It also independently regenerates the final 16B gap as linker output. Whole-module acceptance belongs to the integrator and requires its fresh module/ROM gates; these isolated proofs do not establish that those gates have passed.

The ROM is 674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6. Overlay007 loads at 021D7240 and has 14,144 initialized bytes, hash c8fd4e2dd09fac14b038721acac5ab9053472d0cddf24c44ea0e0cb61a9a629c. Main is the 930,560B initialized ARM9 module with hash ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f. Addresses in this note are qualified by those images and ARM mode.

## Constructor ABI repair

`src/overlays/ov007_20261029_constructors_157d10189451.c` contains only the two 200B/248B bodies. Its measured physical-file SHA256 is 7f6fe72497d257ac810a8ae3ccbe302c79a17708e12d1b98b4db2ba7c7ec7895; the filename stem was computed from normalized LF text. `evidence/matches/ov007-20261029-constructors01.json` records fresh compiler flags, complete source/object/span hashes, ELF relocations, typed native bindings and genuine pinned MW linker artifacts for both functions. Every linked caller byte matches. There is no assembly or opcode patch in the reconstructed bodies.

The decisive correction was the missing R1 parameter of main 0204854C. Its first argument selects a cache bank. Its second is the full 32-bit record index. It finds the first free eight-byte lease at bankBase+0x320, stores bankBase+100*recordIndex modulo 2^32 at lease+4, sets flag bit0 and returns the lease pointer; exhaustion returns 0. The bank base is 020FBAE8+bank*0x3744. The constructors intentionally preserve the preceding SDK index in R1 using MOV. Omitting that argument produced repeated AND-versus-MOV near matches and hid the actual data dependency.

Main02048404 returns the cache index 0..7 or full-word 000000FF. The cached-name and exhausted-slot paths were independently executed 90 times across both banks and all eight indices with randomized scratch/preserved register values. All returned words were zero-extended; FF is 255, not signed -1. The instruction inventory additionally identifies both byte-masked index loops and the cache-loading return block. The latter's filesystem/heap path was not dynamically executed. The C declaration uses an unsigned-byte result, and both constructors store it in a byte field before checking 255. R2=4 andR3=5 are observed arguments; their higher-level meanings remain unclaimed.

Main0204854C was independently executed 104 times across both banks, first/middle/last free lease slots, exhaustion, all valid indices and raw indices -1,0x100,0xFFFFFF00,0x7FFFFFFF,0x80000000. The high/negative index cases verify full-width modulo32 arithmetic and pointer-word stores only. They do not validate those records or dereference the resulting pointers. Negative/high-bit bank IDs are outside the tested constructor domain, and no byte narrowing of the bank argument is inferred.

`evidence/abi/main-cache-sdk-20261029.json` holds these two hash-qualified ABI facts, instruction addresses, full-width returns, argument observations, independent-model results and limitations. The SDK probes give zero new source credit. These prototypes may guide new unmatched drafts; they do not authorize editing accepted source.

The constructor fixture has 90 vectors/180 native-versus-linked executions. Fresh ARM946 machines execute the original SDK string comparisons, lease scans and close/clear helpers. No host callee stubs run. It exercises all-slots-busy returns and cached names with exhausted leases, using null backing allocations so the real native close path avoids heap frees. An independent model checks handle stores, cleared manager lease fields, cleared 100-byte cached records, complete RAM, preserved registers and SP. Native/linked results also agree for every R0-R12 value, CPSR, scratch/stack memory and instruction/write traces. Every execution must actually return within 30,000 instructions.

Allocation/rendering success, cache-miss loading, non-null backing allocation frees, malformed pointers and live scene state remain unsupported execution contexts. Complete source/relocation/link equality covers both whole bodies, independently of that bounded execution scope. Manager and buffer field names are conventional labels for measured offsets, not confirmed UI meanings; the words at 020FEAE8+0x540 and 02101AE8+0xC84 are measured stores of 1. Manager021DA9DC is only four-byte aligned; no invented 32-byte declaration alignment was used.

## Palette caller

`src/overlays/ov007_20261029_secondary_palette_84c0ecdaf642.c` reconstructs021D7D7C/104B. `evidence/matches/ov007-20261029-palette01.json` contains its fresh exact compile/link and 91 vectors/182 actual-return executions. Actual native SDK/CPU-copy callees execute. The independent model checks palette caches, palette VRAM, map cache, character VRAM and the update flag. DMA channel 020DCB44=-1 selects native CPU copies; display controls and VRAM are explicit mapped-memory models. Physical timing, display and DMA behavior are unclaimed.

The corrected secondary state layout has map length at +4, palette pointer +0C, map pointer +10, tile pointer +14, tile length +18 and palette length +1C. The zero palette entry is passed by pointer. Retained earlier drafts have incorrect field/prototype hypotheses and are not accepted source.

## Regenerated16-byte gap

`prove_ov007_alignment_20261029.py` and `evidence/linkage/ov007-20261029-alignment.json` rebuild the unchanged accepted typed data source using the real MW linker. The resulting 2324B range 021DA06C..021DA980 matches exactly, including the 16B gap021DA0B0..021DA0C0. The canonical LCF emits a four-byte zero ctor sentinel and 12 bytes of 32-byte alignment fill. A pure 16-byte alignment fill is byte-equivalent; the original historical recipe cannot be uniquely recovered from these zero bytes. Omitting ALIGN32 moves the data and fails the comparison.

The fresh data object has no executable text or undefined externals. No configured function or module-qualified incoming branch overlaps the gap. The proof does not supply a byte array for the gap and grants zero authored source credit for its 16 bytes. The failed absolute-selector LCF experiment is retained beside the corrected local-object-selector replay.

After integration, the measured inventory can account for 100 functions / 11,820 text bytes, 2,308 authored typed data bytes and 16 independently regenerated linker bytes, totaling 14,144 initialized bytes. The 16 generated bytes must remain distinct from C/data credit. BSS is 2,400B and is outside initialized-byte coverage. These totals describe the proposed complete inventory; accepted build reports determine its integration status.

## Replay and retained failures

Run from the repository with pinned Python 3.13.5 and Unicorn 2.1.4:

```text
python match_ov007_20261029_constructors.py
python match_ov007_20261029_palette.py
python prove_ov007_alignment_20261029.py
```

The scripts resolve all paths through their own repository location. Their outputs are isolated under `work/ov007-finish/20261029/`. The constructor source, fixture and matcher are comment-free and each is below 500 physical lines. Existing source, shared ledgers/builders, application files and original inputs were not edited by this lane.

Prior failures remain under `nonmatching/ov007/20261029-finish01/` and the corresponding work tree. They include bounded unsigned-byte/word locals and returns, early/nested/goto flows, enum/bitfield/union alternatives, partial volatility, C++, multiple optimization levels, compiler families and symbol modes. The closest old constructor results were 197/200 and 245/248 bytes with a single register-mask difference. They are superseded by the measured second-argument repair. No failed near match is counted as source recovery.

Coordinator acceptance: cohort 34 passes all 20 module comparisons, exact ROM layout/hash and negative acceptance checks. Overlay7 is source complete with 14,128 initialized C/data bytes, 16 bytes regenerated by the verified production linker-control interval, and 2,400 BSS bytes. No original executable/data object scaffolding remains in this module. `linker_layout_regions.py` checks the current LCF recipe, ELF boundary symbols, input/output identities, dependency pins and absence of source/object references in the metadata recipe. `verify_linker_layout.py` rejects nine altered/overlapping/stale cases. The 16 metadata bytes carry zero ordinary source/function credit; historical recipe ambiguity and bounded hardware-execution limits above remain explicit.
