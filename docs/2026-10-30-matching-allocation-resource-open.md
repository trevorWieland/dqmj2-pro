# Matching allocation resource initializer

Main ARM`020788F0..02078940` is an exact80-byte ordinary-C candidate at `src/mechanics_save/20261030_allocation_resource_open.c`, source SHA-256`0d0169ad568655a61fa654ef9c90b97988a9586437d63db0cac568a74f5ff8c5`. Canonical report `evidence/matches/mechanics-save-20261030-allocation-resource-open.json` SHA-256`9d13d7e9c8a0e95c0d4fa59d8a46484612182ec4d7bdc5d68b055ba004cfc2ca` matches from repository and unrelated working directories. No source is registered by this replay.

```text
python match_mechanics_save_20261030_allocation_resource_open.py
```

The matcher accepts repository-relative `--source`. Source scratch is a genuine32-byte array; a4-byte outgoing stack argument accounts for the native36-byte local frame. It calls `0205DB90(buffer,020DE42C,-1)`, then `0205D9E8(1,buffer,020DB218,020DB214,1)`, stores the resulting full word at`021C6230` and returns that same word. The first formatter's actual return contract is a pointer to its destination buffer and is declared accordingly, although this caller discards it.

The four literal words are read directly from the measured native span and asserted. Initial exploratory source incorrectly interpreted three addresses from disassembly rendered over literal data, yielding75/80 bytes and the wrong globals. That source/hash and negative comparison remain preserved; no literal instruction patching was used. `020DB214` and`020DB218` are configured data containing count2 and table address`021C67AC`, not callbacks. The actual handle slot is`021C6230`.

The independent worker's frozen native generator/report hashes are`5feba6f3cb0e8b4cb2ee88ad4b09825cc8e95a218bb8d8e705d19453a3413ebf` and`b7a428488e6cf449120a6d8d3a47d420ed8fa6e6d3480e6d28b1c86498424cbd`. New paired replay keeps original52-byte formatting helper,176-byte opener, sprintf/strlen/memcpy/factory wrappers and128-byte two-section splitter. Only four lower functions remain bounded providers: `0200BD04`, `0200BFE4`, `0203CD2C`, `0200C02C`.

All36 native/C pairs return:72 source-entry host returns,72 separately observed formatter returns and72 opener returns. Payload splitting, original factory-handle forwarding, global handle word, two pointer-table words, raw call frames, ordered writes, canaries, poison tails and saved-state invariance match. Nonzero open value256 follows the same successful branch as1; open0 and factory-return0 are distinct measured failure conditions. The stored/returned word remains the original factory handle rather than an advanced split pointer.

Native formatting produces bytes `msg_skillhelp.binJ` plusNUL in19 bytes, leaving13 poison bytes unchanged. The nested32-byte buffer copies the prefix and replaces the final byte withA. These are observed bytes and transformations, without a physical filename-existence or locale claim. The synthetic payload's delimiter selects two pointers without modifying payload bytes. The five direct-helper length controls and three unsupported bounds controls remain separate zero-source evidence in the original report; they are not counted as C80 executions.

Fixture report `evidence/application/allocation-resource-open-fixtures-20261030.json` SHA-256 is`01b0fc12ad7b914274fba4674b9901cc1723228fc2d4bd76b3dd262845886e13`. Source compilation and genuine pinned MW linking compare all80 bytes. Physical filesystem/allocator context, complete scene reachability, whole-module acceptance and global source-credit updates remain separate. Application/baseline/input files, accepted sources, registry and source preferences are unchanged.
