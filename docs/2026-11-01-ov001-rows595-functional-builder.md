# 2026-11-01 overlay001 0222CF34 functional source frontier

## Source status and identity

ARM overlay001 0x0222CF34/780 belongs to ROM SHA-256 674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6 and module SHA-256 39fc7aab33ce02b1910cb8fac58dd9e19936c468f3d03d1ec17dfdc8fe40ce92. Accepted110 v2 has no overlapping source. The newly compiled ordinary C remains nonmatching: real pinned MW linkage emits736 bytes with96 equal same-offset bytes against780. It earns zero exact functions/bytes. All732 original instruction bytes execute; all twelve four-byte pool words have decoded unconditional PC-relative loads whose reader PCs execute. No byte-encoded executable source or assembly is authored.

Run `python prove_ov001_rows595_20261101.py` from this repository or use its absolute path from another directory. Source, context and independent model hashes are pinned. Generated sources and frontend exports remain separate from the final readable C hypothesis.

## Behavior qualification

192 original/freshly compiled and genuinely linked C pairs pass384 actual top returns,5438 watched actual native dependency returns and3326 explicitly supplied service calls. The native RNG, unsigned-state update, soft-float arithmetic, binary32-to-binary64 chain, ceiling, signed conversion and signed quotient/remainder execute as original code. Nested helper returns beyond the named watched entries are not added to those counts. The six supplied boundaries are base-record lookup, category lookup, candidate predicate, optional-resource open/close and final output collection. Their exact prepared word views and distinctive returns are recorded; no supplied call is counted as native.

Independent models agree on every RAM effect outside the disposable stack, ordered non-stack writes, every prepared service word, every actual RNG result and the final explicit physical R0 forwarding from the supplied output boundary. All captured ARM core registers and CPSR also agree except LR, which records the different own callsite. Every raw register/call/write record is retained. The two different executable images naturally remain different in RAM; each complete after-image is validated against its own before-image plus independently modeled effects.

Three wrong C bodies actually return and fail: RNG limit254 instead of255, first byte read from base-record offset0x5E instead of0x5F, and a wrong signed scale increment. Full positive and negative traces are deterministic hashed gzip; the compact report contains per-case counts/hashes and exact mismatch metadata. Normal and alternate-CWD artifacts are byte-identical.

## Measured row flow

The function indexes132-byte rows at0x022498FC. It writes the byte from supplied base record+0x5F into row+0x7A, then repeatedly calls actual RNG with limit255, adds1 and narrows to an unsigned byte. A supplied predicate and comparison against earlier ID bytes decide whether to append. Category responses0,1,2 select total counts3,4,5. ID/value pairs occupy row+0x7A/+0x7B with stride2. These are observed raw IDs/values; their game meanings are not assigned by this test.

The signed16 field at row+0x3C starts at count*50. An optional supplied byte array contributes finite binary32 ratio/multiply, binary64 widening/ceiling and signed-conversion results. The outer modifier threshold is unsigned, while the inner division by100 uses the signed interpretation of modifier-40, as proved by native SMULL/sign correction and independently shown by Ghidra. The product is stored as low16 and capped at999. Signed quotient/remainder by the count then produces each pair value, with the quotient capped at100 before remainder increments. Some synthetic cases produce raw value101; this is not an application constraint or an observed game scene.

The final call prepares four words: signed16 row+0x18, unsigned8 row+0x1A, the pair-list pointer row+0x7A, and output pointer0x0224983C+index*0x40. Its provided return word is physically forwarded. Public prototype and original semantic return meaning remain unproved.

## Frontend repairs and ordinary caller limits

The weak draft had a byte-array declaration for a native 32-bit word table, wrong scaling for byte-addressed signed16 fields, erased scalar/wide arguments, and an unsigned division guess incompatible with native SMULL. Fresh measured contexts restore the table word access, explicit byte-offset signed16 fields, real f32 values and verified f64 R1:R0 pairs. Historical raw M2C output, errors and rejected intrinsic rebinding are preserved; pinned frontends are unchanged. Unseeded Ghidra independently gives the same load widths and unsigned-guard/signed-inner-arithmetic distinction but also erases the wide chain. A separate void-return hypothesis does not improve compiler similarity and stays uncredited.

One direct ARM BL caller is found in module001 split assembly at0x0222CD00. It clears396 row bytes and192 output bytes before dispatching four per-row stages, including this routine. It overwrites R0 immediately after this call. Actual main0x020C5938 supplies that caller's forwarded modifier by zero-extending a16-bit read from0x021D637C. The new caller source/proof is a separate packet; neither this static connection nor the synthetic contexts proves ordinary scene reachability or a current modifier/RNG value. Thumb, cross-module and indirect caller inventories remain separate.

Supported tests use category0..2, row0..2, supplied file counts0..4, ample supplied candidate pools, four explicit RNG seeds, duplicate-first-ID cases, optional resource absence/presence, high-bit field words and modifier0,40,140,0x80000000. The high modifier is direct-entry evidence outside this known caller's unsigned16 forwarding range. Other category values, insufficient pools, malformed pointers, other row/file bounds, resource loading and full battle/recruitment lifecycle remain unresolved. All ABI projections and source signatures are hypotheses until stronger native/source proof applies.
