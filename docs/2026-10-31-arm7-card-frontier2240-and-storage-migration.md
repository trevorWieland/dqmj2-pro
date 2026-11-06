# ARM7 CARD frontier and compatible storage declarations, 2026-10-31

The packet reconstructs four new qualified ARM functions totaling 988 initialized bytes. It also rebuilds nine earlier functions totaling 1,252 bytes from byte-identical C bodies with a compatible shared declaration. Those nine identities are a declaration migration with zero new coverage. No shared recovery registry, configuration, ledger, application adapter or UI was changed in this lane.

| Host ARM7 WRAM address | Total bytes | Instructions | Compiler literals | Bounded behavior |
| --- | ---: | ---: | ---: | --- |
| 03802E0C | 156 | 148 | 8 | Alignment check, command20, block iteration and result stop |
| 03802F04 | 152 | 140 | 12 | Two-byte command01 plus low input byte, bounded retry loop |
| 03802FFC | 116 | 112 | 4 | Result reset, flag mask, wake targets and optional callback |
| 038032B8 | 564 | 560 | 4 | Nonreturning request/task worker and real scheduler handoff |

The total source-only packet has 13 units, 2,240 bytes, 2,128 instruction bytes and 112 generated literal bytes. Every unit passes fresh MWCC compilation and genuine MWLD linking against its entire original span. Original executable objects, literal-binding anchors, imported native callees and unchanged data provide no new source credit. Whole-module and whole-ROM acceptance remain integrator gates.

## Inputs and reproduction

The authoritative ROM remains 175,959,612 bytes with SHA-256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`. The measured ARM7 WRAM image is `e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c`. The pinned Python 3.13.5, Unicorn 2.1.4, pyelftools 0.33 and repository-local compiler/linker remain required.

From the repository, run `python match_arm7_lane_card_frontier_20261031.py`, then `python validate_arm7_lane_card_frontier_20261031.py`. Both resolve repository inputs from their saved script paths. The profile is `nonmatching/arm7-bulk/20261031/lane-card-frontier2240-final/closure.json`; its companion generator-pins.json hashes 58 runtime/static inputs. Actual compiler and linker arguments and working directories are recorded. The final handoff receipt records the independent invocation from the DQM parent directory.

Canonical matching report: `evidence/matches/arm7-lane-card-frontier2240-20261031.json`, SHA-256 `8cfe6d3b82420cfa9527e249d8c88e7ca8d03547b39208597ee4add182ace916`. Control report: `evidence/verification/arm7-lane-card-frontier2240-controls-20261031.json`, SHA-256 `68fba1b991ee1e081228e1b368ff26403ebc035b38fd497777bf2b914161649b`. All 71 controls pass, including 13 actual changed, same-size C bodies that compile, link to changed bytes, and fail independent runtime models. Current missing/corrupted linked products and trace products are rejected before cached proof reuse.

## Storage declaration and preserved bodies

All current compiler units include the same `native_card_types.h` under `src/arm7/lane_20261031_card_frontier_storage`. CardCommon remains a 252-byte prefix view. CardCommonStorage embeds that prefix first and includes the measured 32-bit flags at offset FC, making the reconstructed storage view 256 bytes. The external common symbol has that storage type; CARD_COMMON names its first prefix member. Converting that first-member address back to the enclosing storage preserves the declared object type and avoids extending a prefix-sized external declaration by a cast.

CardArgument remains a 72-byte prefix view. CardArgumentStorage embeds it first and provides measured words48/4C/50/54 and caps58, making a 92-byte view. Both frontier argument views alias this same storage type. These sizeof values describe reconstructed views. They do not establish either original object's total extent, ownership, complete structure or data-source reconstruction.

The compiled layout probe independently emits and executes size/offset/width measurements, including sizeof the actual common external declaration. It returns `[16,4,8,12,252,256,252,256,72,240,164,72,92,72,76,88,4,4,4,4]`. Five changed declarations are rejected. Probe report `evidence/verification/arm7-card-frontier-layout-20261031.json` has SHA-256 `f1279b5023da68df30eae84a26013fa587a3686b5483b330d0f1d8a80dbfeac2` and zero original-code credit.

The nine earlier C files match the frozen1252 source hashes exactly. Their old declarations, sources, reports and objects remain historical evidence. Integrator supersession must replace the old ARM7 batch rather than register both copies, because the current ARM7 builder consumes all registered batches. This packet makes no registry change. Historical prefix headers referenced recursively by the old1252 history remain provenance inputs, never current compiler inputs.

## Native and compiled execution

The full fresh proof compares original execution with newly compiled and linked C in separate fresh machines. It records 7,120 owned original/compiled normal returns, 1,144 separate resumed-parent SleepThread returns, and 2,288 actual nonlocal context loads. The worker has zero owned normal returns and zero ordinary LoadContext returns. Its two SaveContext returns per execution and the resumed saved continuation are separately checked against complete register/CPSR/service-stack context formulas.

The normal-function oracle tables aggregate 117,976 observed native helper returns. Worker dispatch/task returns and SaveContext events are additionally retained in its per-case records and separate fields; they are not relabeled as owned returns. Parent prerequisites, original transfer caller returns and indirect callback returns remain distinct. The failed one-instruction caps receive no return credit.

The new command cases cover full-word addresses, alignment failures, wrap, result stops, command byte order, low-byte narrowing from full32 inputs, retry persistence and bounded lower sleep calls. Completion cases execute actual original callbacks, original kernel setup and a READY original-created thread under disabled scheduling. The worker executes original create/wake/sleep/save/load paths. Fourteen contexts first pass the actual original receiver before the sleeping parent yields to the worker.

Supported worker starts use receive10 or task0C flags, a READY original-created thread and fresh bounded queues. Tick sleep is an explicit lower provider. The cartridge subcases explicitly use synthetic RAM header control00800000 and static received wordDEADBEEF. These values are fixture inputs rather than measured physical cartridge configuration. No BIOS, physical timing, persistent storage, actual FIFO delivery, scene reachability, save-bank meaning or access/renewability policy is proved. Waiting/busy entries without a task, asynchronous flag producers, FIFO-full retry behavior and physical data-ready timing remain unsupported.

## Request domain and failed experiments

The exact worker C uses a 32-bit variable shift with an explicit supported request contract0..31. It does not supply defined portable C behavior for larger shift counts. Every request at or above16 ultimately follows the native result3 path, but the original ARM register-shift operation and portable C shift rules differ outside the stated domain. Three separately retained defined-C formulations (mask31, guard16 and guard32) compile but fail full native byte matching and receive zero matching credit.

The separate original receiver proof records 22 actual returns. With no pending receive flag, tested ordinary requests2..15 set it. With an already pending flag, malformed32/63/255/256/FFFFFFFF can overwrite the request while the flag survives. Therefore no global request<=31 invariant is claimed. `evidence/arm7/lane-card-frontier-request-domains-20261031.json`, SHA-256 `10543468e352f9ad6086f15c5c87ffca9d737529109c0405adc13f0ab64d05f6`, demonstrates those original effects without executing compiled worker C on malformed requests. This defined-C gap remains an explicit reconstruction/portability question even when a pinned native module links exactly.

An early full proof stopped before publication. Follow-up paired original/original calibration at seed56 isolated a random RAM header control4C363A4B without the required data-ready bit. Both bounded runs remained at the original poll near038030C4 and earned no return credit; timeout instruction counts differ and are not treated as deterministic execution results. The preserved report is `evidence/attempts/arm7-card-frontier-worker-paired-failure-20261031.json`. The later supported context states its synthetic control input explicitly. Original/original calibration alone earns no compiled-source equivalence credit.

Earlier 988-byte draft variants and their compiler reports remain under unique nonmatching/work paths. The final case order and ordinary declaration lifetimes yield exact code without instruction patches, forced registers or assembly. Current files are frozen; further changes require new paths.

## Transport and remaining work

Run `python audit_arm7_card_frontier_transport_20261031.py`. It checks current source/include/runtime paths, recursive local Python dependencies, both source profiles, body histories and all historical header pins. The four historical callback/page headers omitted from the earlier transport are explicitly present. Generated Work products, private ROM/save inputs and tool binaries are not transported as reconstructed source; documented baseline inputs and fresh regeneration remain necessary.

This is function-matching evidence with bounded execution proofs and a compatible declaration migration. It does not complete source reconstruction, certify malformed protocol portability, reconstruct original data objects or establish a fully rebuilt source ROM. Existing native matches and all previously frozen files remain preserved.

The alternate-CWD run from `C:\Users\trevo\Documents\RecProgramming\DQM` completed successfully and reproduced canonical SHA-256 `8cfe6d3b82420cfa9527e249d8c88e7ca8d03547b39208597ee4add182ace916`. Its real compiler/linker directories remain repository-local. Historical typed C variants and measured closest compiler outcomes are retained in `evidence/attempts/arm7-card-frontier-tuning-history-20261031.json`; they add zero coverage.
