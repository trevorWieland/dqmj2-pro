# Byte sequence arithmetic and explicit forwarded inputs

Measured build; ROM SHA-256 674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6, host ARM9 / main / ARM. Replay from any directory with the pinned Python 3.13.5 interpreter and the absolute path to `match_mechanics_save_20261101_lane_byte_sequence.py`. The canonical report is `evidence/matches/mechanics-save-20261101-lane-byte-sequence.json`;private inputs and accepted historical sources remain unchanged.

The new ordinary-C candidate is main 0207CE3C..0207CFF4, 440 bytes. Native R0 becomes a byte-input base: all indexed reads are LDRB, the first zero ends processing, and the scan never exceeds 64 entries. R1 is a full query word forwarded to the real table readers;R2 is the initial working word. Initial zero returns before input/table access, including a null input. Other null-input behavior is unsupported.

The first generated hypothesis dereferenced a scalar address and did not compile. A measured byte-pointer view compiled 440 bytes but its unstructured top label kept the loop test at the top. An ordinary while condition permits the original bottom-test scheduling and yields genuine 440/440 compiler/MWLD equality under the preserved 2.0 base / O2 / off settings. No register forcing, padding, assembly or opcode modification was used. Final source and every current object/link/native hash are pinned in the canonical report;object/debug provenance remains local to the current replay root.

Ordinary logic processes raw bytes 10, 11..16, 46, FA, 19, 1A and3C in hexadecimal. The first groups invoke the actual lower conditional-halving helpers. 19 forms a wrapped 32-bit triple, divides its signed interpretation by 4 toward zero and floors the result at 1; 1A applies the analogous signed half/floor; 3C doubles with 32-bit wrap. The final real 0207D144 scans the same prefix: presence 79 takes priority over 02, which takes priority over 7A, selecting factors 2, 3, 4 respectively. These raw codes are not newly assigned game meanings.

The real 0207AFEC returns supplied_table_base + 40 * full_query modulo 2^32. Synthetic 40-byte rows exercise the nibble at +08 bits 8..11, bytes +1E,+1F,+20,+21 and the explicit query-word comparisons in 0207CFF4. The setup uses the measured pointer slot 021C6748, independently decoded from the getter literal. It does not establish original table loading, valid IDs, ordinary scene reachability, producer capacity or ownership. High-word modular-stride aliases are compiled-ARM contexts;they are not portable-C overflow claims for the retained historical signed-index getter.

Four separate zero-credit alternatives retain their entire original bytes while making real inputs explicit:

|Entry|Bytes|Qualified change|
|---|---:|---|
|0207D0C8|48|Forward the actual query to 0207CFF4|
|0207CFF4|212|Forward the query to its first 0207AFEC call|
|0207D0F8|76|Forward the query to its first 0207AFEC call|
|0207D144|84|Use the consumed const-byte-list pointer and pass it to the first 0207B674 call|

All four historical files are hash-pinned and untouched. Two unchanged accepted leaves, 0207AFEC/24 and named saved_feature_occurrences at0207B674/56, are freshly compiled and genuinely linked;their 80 bytes add no coverage. Replay uses committed static leaf/source descriptors, not a generated identity-export prerequisite.

The oracle has 4,760 independent profiles. Each runs a fresh original machine, an exact own-C machine and an all-typed-C closure machine: 14,280 top-level returns and 251,940 separately observed actual helper returns, with zero function providers. Every own instruction address is fetched. The independent model checks the raw result and every lower return, with input/table/global bytes unchanged and no non-stack writes. SP, callee-saved/control state, complete positive registers/flags, read/helper traces and stack canaries must agree. The matrix includes all256 input-byte values, all first-zero positions 0..64, last-position behavior, category/flag branches, signed working-word boundaries, ordering, wrap, final precedence and bounded full-query aliases.

Four complete wrong-C bodies are genuinely MWLD-linked at isolated 026D0000. All 644 wrong executions return;the corresponding fresh original and exact-C positives also return, for 1,932 total control tops. A shortened cap, missing zero floor, truncated query or omitted final multiplier produces 95 independent raw-result rejections and 549 positives. Original functions, code/data bounds and logical data limits remain active. Generated per-case records are deterministic gzip sidecars with declared hashes and uncompressed digests.

The initial leaf-builder attempt used an address-derived symbol for the already named occurrence helper and stopped before native validation. This was corrected to its actual frozen C symbol. An unexecuted setup draft also misread the getter literal as 021C6448;the accepted setup uses the decoded 021C6748. Neither attempt receives validation/source credit. There is no save-bank, chronology, persistence, Windows/Android, whole-module or whole-ROM source-completion claim. Only 440 bytes are new candidate coverage;the 420 bytes of typed alternatives and 80 rebuilt leaf bytes are zero credit until the integrator explicitly selects and validates them.
