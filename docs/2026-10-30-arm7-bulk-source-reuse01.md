# ARM7 ordinary C bulk pass and seven bounded child-WRAM units — 2026-10-30

Seven qualified utility-child ARM7 functions rebuild from standalone ordinary C, link through the actual pinned `mwldarm`, and reproduce all 252 original initialized bytes. Their 560 synthetic profiles produce 1,120 separately observed original/source returns. Root independently reproduced the exact canonical publication, all native proofs and all 22 controls, then registered the seven units for cohort 51. Cohort 51 now accepts the combined module build with all seven source instances selected; this is not a whole-module source-completion or full-game completion claim.

| Program and module | Address / mode | Bytes | Measured field operations |
| --- | --- | ---: | --- |
| `dwc/utility.bin/move/child.srl`, `utility-child-arm7-wram` | `037FC994`, ARM | 48 | Read container word 0; replace it with node word 0x10; clear following-node word 0x14 or container word 4; return removed word. |
| Same | `037FCA24`, ARM | 52 | Use node link 0x64 and following-node word 0x60; when no following node, also clear removed-node word 0x5C. |
| Same | `037FD6C4`, ARM | 40 | Update an optional pointer-to-slot from node word 4, then reread node word 0 and update its reverse slot. The raw return differs between the null/non-null following-node paths. |
| Same | `037FCD90`, ARM | 36 | Relink words 0x10/0x14 and container words 0x6C/0x70. |
| Same | `037FCDB4`, ARM | 36 | Append through container word 0x70, store node words 0x14/0x10, and update container word 0x6C when needed. |
| Same | `037FD6EC`, ARM | 28 | Store pointer-to-slot in node word 4, clear node word 0, and optionally write the node into the supplied slot. |
| Same | `037FF988`, Thumb | 12 | If the incoming pointer is nonzero, clear words 0x48 and 0x4C; return the original pointer word. |

These are field-shape descriptions. They do not establish scheduler, game, ownership or scene meanings. Four instances reuse previously accepted ordinary C implementation families with names rebound to this program; no new algorithm-family novelty is assigned. Source is in `src/arm7/20261030_bulk_reuse/`. It contains structured C memory operations and conditions, no assembly, executable blobs or generated instruction transcripts. The checked compiler target is 32-bit ARM7; pointer-to-word conversions and field accesses require a separate address abstraction before an Android ARM64 port.

## Reproduction and frozen inputs

From any directory, run the pinned Python 3.13.5 executable with the absolute repository script path:

```
python C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\publish_arm7_bulk_20261030_reuse01.py
python C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\validate_arm7_bulk_20261030_reuse01.py
```

The matcher recompiles the seven C files, splits their actual compiled symbols without changing instructions or relocations, and invokes real `mwldarm` under explicit ARM7 settings. No original object or executable bytes enter compilation or linking. The ROM is an independent comparison/oracle input. This batch has no caller relocations, no external callee anchors, no source include dependencies, no literal-pool bytes and no padding credit. It does not establish interworking for an ARM7 caller with external relocations.

The source/compiler closure is `nonmatching/arm7-bulk/20261030/reuse01/closure.json`, SHA-256 `f617074c838757dc5588cca5145e697d8761282f22b8ceaa8763507e435f2a4b`. Generator and local Python/ELF/Unicorn dependency files are pinned separately by `generator-pins.json`, SHA-256 `4543fc97d959d5326ddfc00ae267c5b8a6f0339fe490cfa66348bfc13fd3e1e0`. Python 3.13.5, Unicorn 2.1.4 and pyelftools 0.33 are checked before replay. Compiler hashes/flags and source hashes are explicit per unit. The linker hash is `bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74`. Existing local license configuration is used unchanged.

The frozen canonical report is `evidence/matches/arm7-bulk-20261030-reuse01.json`, SHA-256 `d3a97e12fe22f753bc31fdf27d2e18c535c3764c055863abea572419fddba6c9`. The publication entry point performs fresh builds and all native proofs, then atomically regenerates that canonical report; it does not copy or trust a previous canonical result. The underlying matcher remains available for separately named work-only experiments. The publisher has also passed from the parent working directory, regenerating the same canonical hash. A separate named parent-directory matcher replay is preserved under `work/arm7-bulk-20261030/parent-cwd-reuse01/`. Pre-publication report/control versions are retained under `work/arm7-bulk-20261030/reuse01-pre-publication/`.

The publisher is `publish_arm7_bulk_20261030_reuse01.py`, SHA-256 `fc7644ad43143db28672f8f03d522d67ed878b3bd604db169e07a897717340d6`; its unchanged matching backend is SHA-256 `55212b4f1e7c4030fa2ed7ccc4ed771fd6162350b8abc4979d22079f4810efbb`. Full object/report hashes can differ with output/debug paths or repository roots; current code ranges, frozen source closure and independently reproduced execution records are compared instead of treating an older object's debug hash as universally stable.

## Native evidence and controls

Each execution creates a fresh Unicorn TI925T ARMv4T surrogate, initializes independent GP registers, CPSR, guarded stack and synthetic RAM, and requires the actual LR return address. The source and original executions compare all mapped RAM/code/stack/return-page hashes, all GP registers, CPSR and ordered writes. An independent field-operation model checks RAM, write order and raw R0. Profiles include null/non-null links, selected self/overlapping-node aliases, differing pointer-slot values and signed register bit patterns. No provider or PC-return substitution is used. Each decoded instruction address is visited; merely visiting a predicated instruction is not claimed as proof of every possible program state.

One-instruction exhaustion and invalid-pointer faults are recorded separately with zero return credit. They establish neither valid-record status nor supported arbitrary pointer graphs. All mapped successful profiles are synthetic; this is not DS hardware, scene reachability or concurrent-scheduler evidence.

Current Ghidra roots/ranges are checked exactly. Configured ARM7 direct branches into each unit's interior and initialized aligned words pointing into an interior are rejected; current instruction modes and decoded sizes are measured. Opaque computed pointer producers remain outside this entry-domain proof, and there is no complete-program CFG assertion.

The standalone validator re-executes the native/source profiles independently and compares the complete recorded evidence, including state hashes. Its native cache lasts only for one validation process; input/product hashes and availability are checked again on every call. This permits fresh reports from another checkout without accepting stale original-object hashes or discarding native effects.

It also has 22 rejection controls: wrong processor/program/module/mode/root/extent, changed target/module/source/object hashes, missing objects, a rehashed corrupted ELF body, independently compiled changed C return logic, false return counts, exhaustion misclassified as return, missing linked products, product-path escape, omitted native profiles, fabricated native state hashes, omitted generator/runtime pins, false canonical-publication claims and invented roots. The earlier 19 controls passed before publication, and their versions are preserved. Root independently passed the final 22-control suite after its own publication replay; results are in `evidence/verification/arm7-bulk-reuse01-controls-20261030.json`. Mutation outputs are confined to the new work directory and receive zero source credit. Original code, accepted source, earlier proofs, baseline and application files are unchanged.

## Broader pass and remaining work

The initial audit omitted some registered `functions`/`functionMatches` rows. Its source and report are preserved as inventory-v1 snapshots; the corrected audit uses the canonical entry enumerator and excludes all accepted overlapping ranges. The resulting heuristic backlog has 472 host ARM7 candidates/114,504 bytes and 476 child ARM7 candidates/106,722 bytes. These are configured candidate extents, not the full uncovered initialized-byte denominator supplied by the integrator.

The initial 2,880-profile historical-source sweep and 14,729-object read-only relocation-pattern scan found no new eligible match. A 210-compile option sweep of the 128-byte `027E1F4C` near candidate also failed; a typed-layout alternative produced 136 bytes. All remain negative, zero-credit work. No instruction differences were patched or excused.

Fresh broad host/child hypotheses and compiler journals are under `nonmatching/arm7-bulk/20261030/` and `work/arm7-bulk-20261030/`. Their compileability is tracked independently from byte matches. Old generic host global declarations caused invalid pointer expressions; a separate version used measured array-address contexts, preserving the earlier failures. The broad pass also has genuine but not yet adopted host candidates, including `027E5BAC`/176 and `037FEE58`/108. Their callee, input-domain, data-region and native-effect obligations remain open. This note assigns no credit to them or to original-object scaffolding.

Cohort 51's later workspace scan caught six unregistered outputs containing m2c missing-BX diagnostic stubs. Their bytes were preserved unchanged under `work/generated/arm7-bulk-rejected-20261030/`, removed from the authored candidate tree and assigned zero source credit. `evidence/verification/arm7-bulk-source-policy-cleanup-20261030.json` records each original/preserved path and hash, a clean policy scan and measured unchanged adopted pins. `arm7_bulk_source_policy_20261030.py` now rejects comments and unsupported diagnostics before `draft_arm7_bulk_20261030_v4.py` publishes a candidate; the new canonical reuse index applies the same guard. Fifteen controls, including all six preserved raw stubs, pass in `evidence/verification/arm7-bulk-source-policy-controls-20261030.json`. Historical writers/journals remain preserved. This does not change any accepted C source or generator pin.
