# Word-table predicate and byte scan

Run `python match_mechanics_save_20261101_lane_table_leaves.py`. Two newly reconstructed ARM functions, main 0x0207B004/40 and 0x0207B768/40, match complete native bytes after genuine MWLD linking. The source uses measured word and byte views; both older scalar-as-pointer drafts remain preserved. Registration and whole-module acceptance belong to the integrator.

The first routine reads the pointer word at 0x021C6744+4, then a full 32-bit word at that pointer plus index*40 bytes. It returns whether the incoming mask intersects that word. Its new C uses unsigned multiplication to preserve native address wrap without signed-overflow assumptions. Synthetic preceding backing supports index -1; this is not an application index or table-capacity claim. Indices 0, 1, and 15, all single-bit masks, high-word values, zero, and overlapping masks are covered.

The second routine takes an explicit byte pointer and returns the first zero index among offsets 0..63, or 64 if all are nonzero. Every possible first-zero index is covered with low and high nonzero byte encodings. A one-byte zero buffer demonstrates that the native path stops before reading later backing. No string encoding or valid original buffer extent is inferred.

The matrix has 1,325 contexts and 2,650 actual original/compiled returns, no helper providers, no data writes, complete own-instruction coverage, precise read-order checks, isolated register state, bounded fetch/read checks, stack canaries, and actual return verification. Two complete wrong C variants replace the word read with a byte read and shorten the scan limit to 63. Their eight contexts give 16 actual returns, four measured rejections and four positive coincidences.

Native input, source, current object, linked output, compiler/profile, linker, and replay dependencies are hash-qualified separately. Complete vectors use deterministic gzip sidecars. This adds no save-bank selection, chronology, item meaning, scene eligibility, or unknown-save-byte interpretation.
