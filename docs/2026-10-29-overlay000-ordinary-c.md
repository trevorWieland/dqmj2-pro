# Overlay000 ordinary C recovery and measured return ABI — 2026-10-29

This recovery contributes 23 newly reconstructed ordinary C functions covering 1,292 initialized native bytes. Every entry passes full byte/ELF-relocation comparison and a genuine pinned MWLDARM isolated-caller link. The module still contains an executable backlog; an isolated caller link is not a completed source module or whole-ROM match. Existing accepted sources and headers were preserved.

## Reproduction

Run these repository-local commands; each resolves all paths from its own location:

```powershell
python match_ov000_20261029_leaf.py
python match_ov000_20261029_registries.py
python match_ov000_20261029_halfkeys.py
python match_ov000_20261029_distance.py
python match_ov000_20261029_clearbytes.py
python match_ov000_20261029_freerows.py
```

All use pinned Python3.13.5, Unicorn2.1.4, MWCCARM2.0 base and the verified MWLDARM. The leaf, half-key and wide arithmetic units use O2/inline off. The four32-bit-key table groups use measured O2 speed/inline off. Actual flags, compiler/object/source hashes and source snapshots are in the reports. Compilation consumes reconstructed C, and linker inputs contain the compiled caller plus qualified symbol bindings. No original executable objects or callee bodies enter these isolated links. Immutable link snapshots remain under the corresponding owned Work directory.

## Source evidence

| Report | Functions | Native bytes | Native/source executions |
| --- | ---: | ---: | ---: |
| `evidence/matches/ov000-20261029-leaf01.json` | 2 | 112 | 658 |
| `evidence/matches/ov000-20261029-registries01.json` | 12 | 688 | 1440 |
| `evidence/matches/ov000-20261029-halfkeys01.json` | 3 | 172 | 816 |
| `evidence/matches/ov000-20261029-distance01.json` | 1 | 76 | 592 |
| `evidence/matches/ov000-20261029-clearbytes01.json` | 1 | 36 | 512 |
| `evidence/matches/ov000-20261029-freerows01.json` | 4 | 208 | 704 |

All 4,722 executions use fresh ARM946 machines, require actual return within 10,000 instructions and compare registers, RAM, private stack and ordered memory/executed-PC observations as recorded by each oracle. Original ROM hashing and stored-overlay decompression are checked independently against the measured module. These routines are leaves: no external callee stubs or other native game routines execute.

The32-byte021D8528 routine returns the saved scalar at global223033C+4C while adding its argument modulo32 to field98. A280-vector matrix covers scalar boundaries and random values. The80-byte021DA484 routine copies49 raw bytes to a correctly sized local signed-byte array and returns one signed element for indexes0..48. Its measured table is0,−1,+1,…,−24,+24; the prior draft incorrectly treated the return as unsigned and had an undersized local.

The twelve functions021DF544..021DF7AC operate on four qualified BSS arrays:2231F64 contains16 records of48 bytes;2231E44,2231C04 and2231D24 each contain12 records of24 bytes. Each record starts with a32-bit key. The recovered helpers test membership, find the first zero key, or return the first matching record+4. Fixtures cover every row, absent keys, duplicate keys, zero searches and high-bit keys. Payload meaning is unknown. Native word loads replace the earlier decompiler hypothesis of byte-array dereferences.

The three routines021E5594,021E5744 and021E577C scan32 records of20 bytes at2232868. Native16-bit keys compare with the low8 query bits. The functions clear all matching halfwords and count them, return the first matching record+4, or write byte3 of every matching row while returning the final row key. Full-word query carriers, high-byte malformed row keys, duplicate/zero keys and byte-value carriers distinguish this behavior from a byte-only interpretation. R1 carrier tests beyond the source u8 scalar domain are explicitly recorded as binary robustness checks.

## Qualified signed64-bit return

The76-byte021D8C34 routine returns a signed64-bit result in R1:R0. It forms three signed32-bit differences with32-bit wrapping, sums their squares modulo64 and arithmetic-shifts the signed64 interpretation by12. The unsigned accumulator avoids signed addition overflow in the reconstructed logic; pinned-target unsigned-to-signed conversion and right shift are measured rather than claimed portable. All296 vectors pass, including37 sums with bit63 set and16 exact aliases between input and the global vector. Both return registers are independently checked.

The qualified ABI record is `evidence/abi/ov000-021d8c34-20261029.json`, referencing an immutable execution/link report. The new isolated typed declaration is `src/overlays/ov000_20261029_return_abi.h`. Existing headers were not changed. This measured signature is used for new ov000 callers; no unrelated wide return is inferred for allocation convenience.

Only configured caller 021E035C currently references this entry. Its new ordinary C draft is `src/overlays/ov000_20261029_distance_scale_draft.c`. It remains unaccepted because two arithmetic instructions are scheduled differently. The draft explicitly calls measured signed runtime entry `runtime_main_02025f2c`; the rejected unsigned `_ll_udiv` hypothesis is retained only in failed Work history. `native_alternate_entries.binding('main', 0x02025f2c)` now provides a qualified alternate-entry proof for the label 16 bytes inside 02025F1C, with no invented boundary or callee source credit. No compiler intrinsic is silently rebound to this signed entry. Caller source credit remains zero until complete linked bytes and native fixtures pass.

The 36-byte 021E3180 writes four FF bytes at 022322D0. Four 52-byte first-zero-row helpers at 021E54F4, 021E57F8, 021E5C10 and 021E5FC8 use measured record counts, strides and key widths. They return the first empty record pointer or null. Their fixtures cover every empty position, repeated empty rows, full tables and key-width boundaries.

The separate approximate batch `nonmatching/ov000/20261029-broad01/summary.json` processed 904 remaining configured candidates covering 272,572 native bytes. It produced 794 drafts covering 207,832 bytes, of which 643 compile and cover 147,052 bytes. No candidate is an exact match and this batch receives zero accepted executable-byte credit. Replay with `python draft_ov000_20261029_broad.py --workers 3`. Per-candidate reports preserve failures, native/source/object hashes, compiler profiles, similarity and ABI/CFG uncertainty.

Native birth/RNG application context is documented separately in `docs/2026-10-29-overlay000-birth-context.md`. Its execution proof revalidates existing accepted source and adds no new decompilation coverage.

## Limits and continuation

No gameplay meaning is assigned to the raw keys, payloads, global fields or coordinate scale. Lookup indexes outside0..48, invalid pointers, interrupts and physical hardware are outside these fixture domains. Complete executable coverage, reconstructed module layout and source-only whole-ROM reproduction remain independent acceptance requirements. Overlay004 allocation-only blockers and their unaccepted behavior proofs are preserved in `docs/2026-10-29-overlay004-allocation-blockers.md`.

Frozen accepted source candidates:

- `src\overlays\ov000_20261029_leaf_9f510e0af6a5.c` — `9f510e0af6a50eb23215a06a8dae17859780cc394a785894ab4117c2d42f2b7e`
- `src\overlays\ov000_20261029_registries_3c92cfe807e5.c` — `3c92cfe807e5ee08a24214b5d3271127927851434b7f78eef7a6026704c53595`
- `src\overlays\ov000_20261029_halfkeys_8d41ce185b7d.c` — `8d41ce185b7d242f931065bc7959d892d90527733ab3b6f196907e58ac584204`
- `src\overlays\ov000_20261029_distance_e298aa833414.c` — `e298aa83341450436f5fa7208dac5284d9f76e144e051658b411ef8db033296e`
- `src\overlays\ov000_20261029_clear_bytes_f193ed4b29bb.c`
- `src\overlays\ov000_20261029_free_rows_c6d833a66a67.c`
