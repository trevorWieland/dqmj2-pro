# Kind loader and new-list-entry count, 2026-10-29

Two additional ordinary C routines compile and genuinely link to 192 measured bytes: main ARM `02044998`, 60 bytes, and ov000 ARM `02210C8C`, 132 bytes. They remain candidates for integrator acceptance. No shared registry, previous source, verifier or evidence report is changed.

Candidate source is `src/encounter/20261029-kind-context/`, with byte-identical hypotheses retained in `nonmatching/encounter/20261029_kind19/`. Its header and two C files contain 13 to 26 physical lines without comments or assembly. The loader uses pinned MWCC 2.0 SP1p5 O2 with speed optimization; the counter uses O2 without that option. Both use ARM946E, inline off, and fresh real MWLD links. These settings are specific measured unit profiles.

```text
python C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\nonmatching\encounter\verify_20261029_kind_context.py
```

The repository-CWD and parent-DQM-CWD replays both pass and produce the same report hash.

| Artifact | SHA-256 |
| --- | --- |
| `nonmatching/encounter/verify_20261029_kind_context.py` | `f77432977daa2e1524e57e33c5364f13cf019cc5fe47126f117c5b45ea85155f` |
| `nonmatching/encounter/kind_fixtures_20261029.py` | `8a54ff0020702f94dd6e95b4047a6749db31a43414d7d4eabe6a0357c0b3d411` |
| `evidence/matches/encounter-20261029-kind-context.json` | `80fb425a5cef7044e0ca593e3919db6f932495a84e283815314148c32410326d` |
| `src/encounter/20261029-kind-context/kind_context.h` | `79161747f8f4d912668f79e820a4fe8979e67d5f170318d3c333f781c235ab0e` |

Every source entry declares and precompilation-checks the exact header closure. The report includes source/object/native-range hashes and complete linker proof. Existing helpers `021E7B08`, `021DFDC4` and `020449D4` are already accepted and receive zero duplicate credit.

## Measured list behavior

The 132-byte routine counts successful **new insertions into a 32-word list at `022351EC`**. It does not query encounter accessibility. Its already accepted helper `021E7B08` first scans all 32 words for an equal key and returns zero if one exists. Otherwise, it stores the key into the first zero word and returns one; if the list has no zero word, it returns zero. Key zero cannot create a new entry.

The counter generates up to two candidates. Field-record byte `+6` equal to 1 selects candidate 150; equal to 0 selects 151; equal to 2 or other values skips that first candidate. If the corresponding kind-record byte `+0x61` is positive, the second candidate is the word read by `021DFDC4` from `0222E29C + 4*(byte61+13)`. The two helpers execute in this order, so equal candidates are deduplicated during the same counter call.

The word view at `0222E29C` is used here without importing meanings from other callers that access its first three words. Neither that view nor the 32-entry list is assigned an asset, party, save-bank, progression or encounter meaning by this evidence.

For example, original field ID 42 maps to kind index 292, whose byte `+0x61` is 14. With an empty list and synthetic translation word 201 at index 27, the actual routine inserts `[151,201]` and returns 2. A repeated call returns 0 and leaves the list unchanged. Other fixtures prove one insertion, full capacity, one remaining slot, existing candidates, duplicate words and a high-bit raw candidate value. The latter tests word identity, without assigning the candidate a valid resource identity.

## Execution and limits

Fresh original-versus-linked-C testing passes 140 actual returning outer calls per implementation, 280 total, using 86 separately initialized machines per implementation. Fifty-six direct state configurations execute twice, and 28 connected SYS10 cases return using the original ROM-backed field/kind files and explicitly manual manager/lookup setup. The counter is reached 140 times per implementation. The direct counter pair with the largest combined count uses 6,710 instructions.

The tests independently model the complete 32-word list and both return counts. They also compare R0 through R12, SP, LR, PC and CPSR, ordered CPU stores, persistent and VM state, actor pool, metadata/cache/lookup data, the unique list and the relevant translation-word view. Counted calls must reach the real return sentinel and preserve SP/R4-R11. No native functions are stubbed. The counter uses the normal 20,000-instruction and one-second limit; the surrounding SYS dispatcher retains its separately declared 100,000 limit.

SYS10 calls this routine only after a successful constructor and ignores its returned count. A new-list-entry count therefore supplies no encounter-access or repeatability predicate. Its list writes remain measured side effects.

The 60-byte kind loader uses `EnmyKindTbl.bin`, stores its handle at manager `020F69EC` and sets manager `+4` to the eight-byte-header-adjusted record base on success. Its full source-linked bytes match, but both true-entry probes with mode 0 and mode 1 fault in the original resource path at main ARM `0200B534` after 146 instructions. They have zero returning calls and no post-fault state proof. Real file loading and handle ownership remain functionally unsupported.

The metadata files and 1,399-entry compact prefix retain their earlier provenance and limits. No initializer is extended to 1,421. Full scenes, rendering, travel, malformed records, native IDs outside the measured domains, story/quest access, script reachability and renewable encounters remain unproved. Whole-module acceptance and whole-ROM source reconstruction remain independent integrator gates.
