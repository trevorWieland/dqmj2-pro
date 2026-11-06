# Complete context/numeric predicate writing primary24, 2026-10-29

One additional substantive 352-byte SCR routine rebuilds exactly from ordinary C with the **unchanged frozen v4 compiler**. It is `s02e10.e` entry102, code `[75216,75568)` / `[0x125D0,0x12730)`, with a private return at75564. The sole known direct script CALL is at99432. Entry102 is its only table alias, and decoded direct transfers reveal no external interior entry or shared return tail.

```c
#include "scr_numeric.h"
void set_primary_24_when_numeric_values_match(void)
{
    float context_value = get_context_value(0);
    float state_zero = get_numeric_state(0);
    float state_three = get_numeric_state(3);
    if (context_value == 12) {
        if (state_zero == 2) {
            if (state_three == 1) {
                set_primary_flag(24, true);
            }
        }
    }
}
```

These are raw measured context/numeric indices, constants and primary flag ID. No area, story, quest, access, acquisition or renewal meaning is assigned. The natural producer of context0=12 remains unproved. The separately documented [s07e01 context producer](2026-10-29-scr-context-producer-and-numeric-validator.md) does not establish this image's ordinary scene path.

## Reproduction and executable scope

```text
python C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\match_scr_primary24_20261029_batch05.py
```

The final paired replay passes from the parent DQM directory. The source-only compiler subprocess receives only the frozen v4 compiler, frozen v1 parser, new C/header and named allocation JSON. It has no ROM/bytecode input. Its 352 emitted bytes match exactly; the complete rebuilt decoded image remains byte-identical. All eight archive members decode to that same image and give no duplicate source credit.

The decoded image contains104,512 bytes. The remaining104,160 bytes, archive storage/compression, interpreted callers and native callees remain zero-credit scaffolding. This recovers one authored definition and one complete qualified instance, with no complete-image or whole-ROM claim. Named runtime bindings independently decode native dispatch cases and their BL targets for SYS39 numeric reads and SYS42 primary writes; original native bodies receive no additional source credit.

## Shared scratch reconciliation

The explicit allocation profile maps `context_value` to146, `state_zero` to138 and `state_three` to139. The reconstructed unit unconditionally initializes each before any branch/read. Slot146 has no known outside read/write. Slots138/139 have outside writes and **three known outside reads**, so they are not described as globally private.

All three reads belong to entry100's separate range `[73888,75160)`: slot138 reads74100/75088 and slot139 reads74136. That entry has no known external interior entry. Its straight-line prefix unconditionally copies fresh SYS39 results to138 at74020 and139 at74076 before its first read74100 and first conditional74124. Consequently those known readers are dominated by their own initialization during serialized complete invocations. The prefix's native APIs47/48 and39 execute unchanged in the fixture.

Three additional independently initialized native controls start actual entry100 with poisoned138/139 and numeric pairs0/0,2/1,255/255. Twelve original script records reach boundary74100; both slots contain the new expected numeric values, and persistent state is unchanged. Each prefix makes14 actual native calls. The prefix boundary is **not** a return of entry100; the enclosing routine is neither recovered nor claimed completely tested. All42 prefix native calls per implementation truly return and are included separately from the complete reconstructed-function scenarios.

Opaque native slot accesses, computed entries and reentrant/interleaved invocation semantics remain uncertified. All known references and the exact dominance qualification are exported in `boundariesAndLocalStorage`; no outside read is hidden or relabeled as a write.

## Native returns, mutation and errors

The final proof passes **3,980 native calls per implementation /7,960 actual returns total**, using132 fresh machines per implementation. There are128 complete-function scenarios, one native negative-entry case, and the three explicitly bounded outside-reader prefixes above. Every counted native call reaches its sentinel within20,000 instructions and one second, preserving SP/R4-R11. Original/rebuilt R0-R12/SP/LR/PC/CPSR, ordered CPU stores, full persistent state and both VM context observations agree without stubs.

The complete-function cases exercise all four nested outcomes, every VM thread, both prior states of primary24, numeric byte extremes, context values adjacent to12, signed zeros, infinities and NaN payloads. Initial scratch poison is overwritten; getter results retain exact binary32 values. The routine reads numeric0/3 regardless of the later predicate and calls the setter only when all three equalities hold.

Primary24 is stored through a **32-bit read/modify/write at0x021C0E20**, setting bit24 and preserving every neighbor bit. A matching second invocation repeats this setter and word store even if primary24 is already true. Its persistent bytes then remain identical. This proves neither a once-ever action nor an acquisition limit. Ten invalid source/profile controls reject bad API indices, Boolean/type errors, invalid/missing/duplicate/unused allocations and unsupported arithmetic. A wrong but valid allocation fails original-byte equality. Broader unchanged-v4 ABI, structured-else and CLI-failure controls remain separately frozen in batch04.

Two failed hypotheses are retained under `work/script-source/20261029/batch05/`: `native-fixture-byte-store-trial.py` plus `byte-store-fixture-failure.json` preserve the incorrect byte-store assumption and measured word write; `private-slot-trial-matcher.py` preserves the rejected assertion that every outside reference must be a write. Neither failure gives source credit. The final proof instead asserts the exact native word write and explicitly reconciles all three outside reads.

## Frozen identities

| Artifact | SHA-256 |
| --- | --- |
| `src/scripts/20261029/batch05/set_primary_24.c` | `9b4fda3074d5326c26642eaac79eb1aaf1072af821e56523c13d3c3a66495506` |
| `src/scripts/20261029/batch05/scr_numeric.h` | `dd9083a3b944895fa04c96a6dc41900e7d9d1923842f1f420ea253ff854a3bcf` |
| `src/scripts/20261029/batch05/primary24.locals.json` | `8e6f6807531deefcc20adfb035ba71ea2416925a91baf11dfea03449e034669f` |
| Frozen v4 compiler | `171818c7eda16c5d44e098a45ec425b268730a38e5f5696b73e19ce5e06b9de7` |
| `nonmatching/script-source/20261029/native_scr_primary24_20261029.py` | `245b0b963e2bc453f0c2ff72040d2c4489759fec0d3d06bc35d921a12e14eb98` |
| `match_scr_primary24_20261029_batch05.py` | `1672c50414bc5b8b0fba6dd3c5eefd41b8ba4be5de53fe987e4e2a05db833aed` |
| Emitted/original352B body | `5656f43fe8369e71cdce73ff171712f2e3e26d165734a2aee94d6c304838ed96` |
| `evidence/matches/scripts-20261029-primary24.json` | `4b6ceafb855537077548d706b1fae286f2594e8841e9e286cca69d8a05ce8e48` |

The image hash is `39a6d7add5e43f7bc403b50cc9ac6a22c17f10c826f6b95760634f2fff65a906`; archive hash is `74d48a6935dd26ed80407785750aa5e976a5517727301ac0c00a7b09f661aa14`. Original ROM allocation and executable hashes are pinned in the replay.

The new v4 audit scans297 images for complete forward private-return graphs and actually compiles ordinary C hypotheses. It finds122 exactly representable nonempty ranges, including prior recovered routines, this new predicate and117 copy/getter-only ranges. Those remaining drafted ranges have zero native execution proof and zero accepted source credit. New authored compiler/backend capability was not needed, and no v5 is introduced.
