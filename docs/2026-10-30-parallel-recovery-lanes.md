# Parallel recovery lanes — 2026-10-30

Recovery now uses four active agents: the integrator and three isolated local Git worktrees. Each lane can run up to three subprocess-isolated draft/compiler jobs. The session has four agent slots; compiler processes are tool jobs, not additional agents. All source, inputs and outputs remain private, with no remote.

| Lane | Workspace | Exclusive new source scope |
|---|---|---|
| Integrator/main | `dqmj2pro-decomp` | Main below `02040000` and at/above `020D0000`; shared registry, ledgers and accepted builds |
| Save/core | `j2p-recovery-lanes/save-core` | Main `02040000..020D0000`, prioritizing persistence/progression/mechanics |
| Overlays | `j2p-recovery-lanes/overlays` | Remaining overlays, separately identified by module/hash despite overlapping load addresses |
| ARM7 | `j2p-recovery-lanes/arm7` | ARM7 and its connected SDK/ITCM/utility frontier |

The worktrees start from source revision `9cd4ac09`. Each has 3,038 copied, independently hash-verified local dependency/input/scaffolding files totaling 483,715,851 bytes. There are no junction dependencies. The bootstrap receipts are `evidence/verification/recovery-lane-*-bootstrap-20261030.json`. Extraction and disassembly remain zero-credit scaffolding. An integrator claimed-range export prevents duplicate drafting of already selected or pending ranges; unsized entries reserve their start without invented extent.

The first breadth waves examined 207 distinct processor/module/function identities covering 173,848 native bytes: 80 main functions / 64,836 bytes, 72 overlay functions / 82,996 bytes, 32 save/core functions / 22,764 bytes and 23 ARM7 functions / 3,252 bytes. The save sweep explicitly distinguishes 24 existing draft reuses from fresh attempts. These figures describe examined queues, not new decompiled source or accepted coverage.

Those waves produced 105 compilable candidates across the lanes. Overlay sweeps alone produced 49 compilable candidates / 50,892 bytes. Compiler-only matches, same-offset near scores, complete native-model evidence and accepted module/ROM credit remain separate stages. An 812-byte overlay candidate and a 396-byte save/core candidate reached exact comparisons during bounded follow-up; they still require independent integration gates.

Workers rotate after roughly ten source variants or ten minutes of isolated tuning, retaining failures and unresolved ABI/object-boundary issues. They start the next queue while exact-candidate proofs run independently where resources allow. Shared mutable compiler state is never used across threads; workers have processor/module/address-qualified output directories. Unresolved carry state, inherited registers, missing object extents and unknown aggregate types remain explicit failures rather than placeholder logic.

Source-only handoff commits contain reviewed sources, fixtures, models, negative controls, metadata and a file/hash manifest. They omit registries, ledgers, project configuration, input payloads and work/build objects. The integrator imports the commit, recompiles/relinks and reruns the native proof before acceptance. Existing matches and immutable source variants remain intact. Complete regressions will use larger accepted batches; broader provisional recovery does not weaken byte, object-bound, semantic, linking or whole-ROM requirements.

The main breadth drivers are `draft_main_breadth_lane_20261030.py` and `draft_main_breadth_round2_20261030.py`; their incremental reports stay under `evidence/attempts/`. Worktree queue ledgers record drafted, compilable, near, exact and semantically tested ranges independently. The goal remains active, and accepted coverage is measured only by the current cohort/manifest.
