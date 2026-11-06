# Main decimal family: reference recovery and native models

Six ordinary C functions have independent compiler, genuine linker and bounded native execution proofs totaling 1,776 initialized bytes. Cohort 93 rebuilt their containing module and accepted these replacements. This document grants no additional coverage beyond that measured acceptance.

The reference is the CC0-1.0 Petari repository at revision `177da59137be40bcca5cd996e013c228ae20b198`, specifically [ansi_fp.c](https://github.com/SMGCommunity/Petari/blob/177da59137be40bcca5cd996e013c228ae20b198/src/MSL_C/ansi_fp.c), its decimal header and [license](https://github.com/SMGCommunity/Petari/blob/177da59137be40bcca5cd996e013c228ae20b198/LICENSE). Unmodified files remain under `deps/msl-ansi-reference-20261031/`; URLs and SHA-256 values are recorded in `provenance/msl-ansi-reference-20261031.json`. These public references receive no source-match credit. The adapted sources are comment-free, separately authored files under `src/runtime/`.

The reference uses 36 decimal digits. The measured DS routines use 32 digits in a 38-byte view; multiplication uses a 64-byte intermediate digit area. This difference is established by native offsets, loops, source compilation and byte comparison. The original structure declarations and semantic use of its sign byte remain unproved.

## Individually matched units

| ARM9 main address | Initialized bytes | Recovered operation | Qualification |
| --- | ---: | --- | --- |
| `02022998` | 108 | Round direction | 512 native/C pairs, all instruction bytes, no helpers/providers |
| `020232C4` | 676 | Decimal subtraction | 393 independent native/C pairs, 786 actual top returns, all instruction bytes observed, no helpers/providers |
| `02023104` | 224 | Magnitude equality | 512 native/C pairs; zero sentinel, exponent and zero-padding cases |
| `020231E4` | 224 | Magnitude ordering | 512 native/C pairs; full signed exponent range and padded significands |
| `02022CE4` | 156 | Byte-string conversion | 512 native/C pairs; truncation and raw-byte rounding cases |
| `02022B60` | 388 | Decimal multiplication | 512 native/C pairs; 384 instruction bytes and one 4-byte literal |

`match_main_decimal_subtract_20261031.py` reproduces the subtraction proof and fourteen actual returning wrong-C executions. `match_main_decimal_family_20261031.py` reproduces the other four proofs, 4,096 actual top returns and 192 actual returning whole-C controls. Each wrong source is compiled and genuinely linked; native bytes are never patched into the reconstructed source object. Helpers called by string conversion and multiplication execute original measured code and receive zero new source credit.

`match_main_decimal_round_direction_20261031.py` adds 1,024 actual top returns and 128 actual returning controls. Its independent integer remainder/half comparison covers numeric digits, lengths 2..32 and interior rounding positions; malformed records are unsupported.

Each source independently matches with the pinned 2.0 base compiler, `-O3`, speed optimization and inlining disabled. The retained profile experiments also find some exact O4 profiles. O2 does not match these units. None of this establishes a project-wide or original compiler configuration.

## Measured arithmetic limits

The subtraction routine does not consistently implement conventional nearest rounding at a 32-digit precision boundary. An initial independent conventional model failed 141 of 390 actual native cases. That failed characterization is retained in `evidence/attempts/main-decimal-standard-rounding-characterization-20261031.json`. The passing fixture models the measured digit-index correction with independent integer arithmetic, including the higher aligned digit decremented for some discarded values. The source preserves that behavior. Exponent differences of 32 or greater can access beyond the supported digit view and are excluded from the accepted fixture domain.

The string converter compares a following raw byte numerically with 5. It does not first subtract ASCII zero for that comparison. The fixture includes raw bytes 1, 4, 5 and 6, ASCII tails and even/odd retained prefixes. No general text encoding, language or conventional string-rounding contract follows.

Multiplication is checked against an independent integer product with 32-digit nearest/even rounding and native signed-16-bit exponent wrapping. The tested domain contains positive nonzero inputs of one through 32 digits and supported destination aliases. Zero multiplication inputs and arbitrary malformed records remain unsupported. Equality and ordering treat a zero first digit as a sentinel and ignore the sign byte in their measured operations; they are not presented as general signed-number APIs.

All proofs compare complete backing memory and relevant register state, require actual bounded return, and isolate machine state for each run. Void subtraction's physical R0 residue is compared without inventing an API return value. Unused digit bytes are compared between native and reconstructed executions but do not all have an independently established semantic meaning.

Adjacent `__ull2dec` recovery encountered unrecognized `_ull_mod` and `_ll_udiv` compiler intrinsics. Its failed profile history remains unaccepted. The frozen symbol resolver, alternate-entry verification and binding guards are unchanged. A future adapter must first establish their measured ABI and entry identities; established compiler matches alone cannot justify them.
