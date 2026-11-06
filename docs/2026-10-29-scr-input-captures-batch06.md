# Qualified input-capture source and fixed-slot ABI, 2026-10-29

Frozen v4 now rebuilds **115 complete input-capture routines / 7,368 physical SCR bytes in 92 decoded images** from ten ordinary C definitions under `src/scripts/20261029/batch06/`. There are six distinct API shapes; raw numeric-index variants remain separate authored definitions. This batch adds **zero substantive decision-logic bytes**. Physical instances, authored definitions, API shapes and meaningful decisions must remain separate progress measures.

Example source expresses ordinary typed input capture:

```c
#include "scr_numeric.h"
void capture_context_0_and_context_1(void)
{
    float value_0 = get_context_value(0);
    float value_1 = get_context_value(1);
}
```

The explicit allocation profile binds each declaration to a VM register-file slot. Native output bytes remain stored after RET; no private automatic-storage or portable Android ABI is claimed. The fixed-slot source backend intentionally emits the declaration assignments, including otherwise unused captured values. This is a documented VM lowering/storage contract, not a claim that an optimizing host compiler preserves unused C locals.

All selected source routines are straight-line getter/capture operations with a private return. The source-only subprocess receives the frozen v4/core, build driver, ten C files, common ABI header and a layout-only table of image hashes, placements and named allocations. Original bytecode is not a compiler input. Generated layout/products and reference inventories live under `work/` or `evidence/`, separately from authored C/header files. No source file contains opcode macros, PC transcripts or executable arrays.

## Exhaustion correction and held unit

The [batch05 note](2026-10-29-scr-primary24-decision-batch05.md) grouped 117 setter-free drafts as copy/getter-only. Detailed classification corrects that historical approximation: **116** are straight captures totaling 7,496 bytes; the remaining **216-byte s08e12 entry51** has nested empty-arm comparisons and remains a separate zero-credit decision hypothesis. No source credit had been granted to that draft index.

Of the 116 straight captures, 106 have no known outside slot reads. Nine more have outside reads reached through known roots whose own writes or guaranteed complete capture-call writes dominate those reads. Every outside read/write, reaching root and initialization result is exported. The analysis is syntactic and conditional on reaching the read; it does not claim complete execution of those other callers. Native opaque/computed slot accesses and interleaved/reentrant scheduling remain uncertified.

One 128-byte routine remains **excluded**: `s03e08.e` entry60 at98788 captures numeric0/5 into slots102/103. Three reads of102 at94808,95848,96124, reachable from root92904, have no known prior initialization. A shared live-in/output ABI or consumer proof is still needed. It is not described as private, silently accepted or given source/byte credit. Other callbacks in that image may still be independently qualified.

## Native execution and reproduction

```text
python C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\match_scr_captures_20261029_batch06.py
python C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\validate_scr_captures_20261029_batch06.py
```

The fresh final matcher passes **10,482 native calls per implementation / 20,964 actual returns total**, with **1,380 fresh machines per implementation**. Every qualified range runs all four selected VM threads and three input profiles. Profiles cover positive/negative NaN payloads, signed zero, infinities and finite raw binary32 context words, plus numeric bytes0,255 and distinct indexed values. Context copies preserve raw words rather than performing numeric conversions.

Each complete routine starts through the original native entry/fork API and executes every source-emitted record through its private RET; PC is not manually forced. Every counted call reaches its native sentinel within20,000 instructions and one second, preserving SP/R4-R11. Original/rebuilt R0-R12/SP/LR/PC/CPSR, ordered stores, full persistent state and both VM contexts agree without stubs.

An independent model constructs the expected complete 256-word VM register file from poisoned initial storage, overwriting only the declared output slots. All other slots, condition byte and persistent bytes remain unchanged. Context input words remain unchanged; numeric getters' argument-register effect is checked separately. Native call order/results, trace length, depth-zero completion and exact private return are retained per unit. Archive member aliases are checked without multiplying source credit.

The final input-separation replay succeeds with no dependency on old draft C files. A prior absolute matcher replay and the final standalone accessor also pass from the parent DQM working directory. Missing or changed source inputs/products must withhold current credit; preserved scaffolding never counts as source.

## Grouped accessor and controls

`validate_scr_captures_20261029_batch06.validate(root, report_path=None)` returns one record per `(codeSha256,startPc)` after one complete current validation pass. It pins the frozen generator/closure, current ROM/native/archive bytes, source and layout inputs, emitted products and all known outside-reference/dominance evidence. It freshly re-emits all C units in an isolated source-only directory, then checks every qualified body, current direct/private boundary and complete native proof record. The held128B unit is explicitly excluded.

The accessor independently rebuilds every input profile, poisoned 256-slot expectation and persistent-state expectation and requires every thread/profile pair. It validates actual-return counts, native call ordering/results and all state-digest records. This is validation of the frozen captured native evidence; the matcher command reruns Unicorn. The integrator may cache its returned dictionary only within one fresh measurement.

Local controls reject an altered raw NaN profile, false other-slot-preservation claim and missing emitted product. The matcher additionally proves that a wrong but valid allocation changes bytes for each of the ten source definitions. Earlier frozen-v4 malformed-source/API/ABI controls remain independently versioned. No backend/compiler capability was changed for this batch.

## Frozen identities

| Artifact | SHA-256 |
| --- | --- |
| `match_scr_captures_20261029_batch06.py` | `ae04eacaea7ad4c626bf028b84079d163b3065365d6ac18420ce4d8dc9164193` |
| `validate_scr_captures_20261029_batch06.py` | `f3d9c1b4dc514ebb0395c19e1f949f12c9c0121fe0d0bf4cb010aac0ad999cb8` |
| `audit_scr_captures_20261029_batch06.py` | `fc80779acc1f97ae8cdae500be2030ea0eea4b78f9d0d1b6b2b97014ce454612` |
| `build_scr_captures_20261029_batch06.py` | `e395d329a5555b0615b0d46a3d97a98b3811bdcc83b806e3753851f6d020c9b7` |
| Native fixture | `46c2cb5ab59d6fc4a39a500420acd8fef8ae0c60007fcb809406c2241d9fa1eb` |
| Frozen v4 compiler | `171818c7eda16c5d44e098a45ec425b268730a38e5f5696b73e19ce5e06b9de7` |
| `evidence/encounter/scr-capture-source-layout-20261029.json` | `73578cd3a74da3fa59b513b030ca4beea649e47a013198fd1d31737d8a378e0a` |
| `evidence/encounter/scr-v4-candidates-20261029-batch06.json` | `769b197a673fe8e067c79299b31d53f88873ed333fd1d651f53eab1221a3b9bf` |
| `evidence/matches/scripts-20261029-captures.json` | `61d1669372d6e6a0c38d58d4e83d4781f0240111e132bab051854573179f8d1a` |

Per-definition C/header hashes, per-range products, allocation profiles, image/code hashes and reproduction commands are in the report. No full image, native executable bytes, archive compression, scene, story meaning, encounter availability or renewability is established. Baseline/application files and previously frozen sources remain unchanged; shared ledger acceptance is integrator-owned.
