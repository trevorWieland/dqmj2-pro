# DQM workspace cleanup — 2026-11-06

Deleted 169 verified disposable decomp replay and clean-build copies. The observed net free-space increase was 248.69GiB, leaving 249.82GiB free. All planned targets were verified absent; original ROM/save input hashes and the main measured ROM still match.

The four visible project folders are `design-system`, `dqmj2pro-decomp`, `dqmj3pro-decomp` and `monster-fieldnotes`. The unique `j2p-recovery-lanes` and `monster-fieldnotes-windows-rewrite-reference` directories remain preserved and hidden. No actual project root was deleted.

The first hiding-only pass reclaimed no space and was superseded by this deletion. Its old attribute inventory remains historical evidence, not a promise that deleted disposable copies can be restored.

[The pruning receipt](../evidence/workspace/dqm-replay-copy-pruning-20261106.json) records every deleted path, input checks and observed free-space measurements. The reviewed plan, executed script and final result are preserved beside it. The main decompilation workers and sealing process continued independently.

New copied-root proofs belong under `work/copied-root-replays/<unique-name>`. Preserve the main proof receipts, logs, hashes and immutable inputs, then prune completed disposable copies after checking live processes and runtime dependencies. The root `AGENTS.md` records this retention rule so completed sandboxes do not accumulate again.
