# Clean proposed-source and duplicate-proof replays

The clean-X source build completed 778 commands before the historical proposed sequence validator tried to hash an object that no command had regenerated. Its frozen source matcher was retained as evidence but was absent from the oracle replay command. Source matching, linked-byte checks and native execution were sound within the original workspace; their historical object cache was an undeclared prerequisite for this validator's entry point.

`replay_arm7_seq_main_proposed_clean_20261031.py` runs the pinned proposed producer before the entire unchanged validator. Each invocation starts with an empty dedicated directory beneath `work/arm7-bulk-20261030/seq-main-clean-replay-20261031`. An explicit directory must be empty and remain inside that scope. The default creates a new UUID-named directory. No object, ELF, linker output or compiler cache is copied. Paths are resolved from the wrapper's own repository, independently of the invocation directory.

The wrapper changes only four in-memory output locations: `matcher.WORK`, `validator.REPORT`, and the two modules' report writers. Compiler, linker, fixture, validation and rejection functions remain intact. The writers reject unexpected output destinations and redirect exactly one producer report and one complete validator report. The original 91a25bd6 proposal report and 2f2d94ca control report remain byte-identical, preserving the accepted boundary-review history and its existing pins. The four output globals are restored in `finally`. Frozen entrypoint stdout is retained as historical text, because its final print statements still name historical destinations; the wrapper's receipts hash the actual redirected reports.

All 36 original negative controls pass. Four additional checks remove the newly compiled object before validator caching, remove it again after caching, require positive validation after restoring those exact bytes, and reject reuse of the populated output directory. Every full proposed execution proof retains 790 actual original/compiled outer returns and 211,774 separately observed nested returns. These are per-proof counts, not additional source credit. The wrapper does not grant boundary approval, module credit or another 352 reconstructed bytes.

The first lane attempt stopped before compilation because lane bootstrap had omitted the old proposed C input. The corresponding historical file already existed in Root and X. It was restored locally from byte-identical accepted C with SHA-256 `830288c663af1edf3a81c357df69da0e2f40668c377b39848611a182a95fd181`. No old generated product was copied. This separate lane omission and its repair are preserved in `evidence/attempts/arm7-seq-proposed-replay-lane-input-20261031.json`.

The proposed replay passed in the lane and again from `C:\Users\trevo\Documents\Codex\2026-10-26\files-pasted-by-the-user-separate`, using separate initially empty output directories. The first receipt and final receipt are retained independently. Generated products remain in their declared work directories and can be regenerated from source.

## Other registered validators

The read-only AST/report audit covers Root's 199 current oracles and clean X's own 182-oracle registry. It recognizes direct product checks, local validator imports, literal evidence inputs, producer registrations and repository-qualified generated-product paths. Eight synthetic controls qualify missing products, producer registration, cross-checkout Windows paths, real input versus generated-object distinctions, present products and explicit large-report withholding.

Using X's own regenerated reports removes cross-checkout debug-object false positives. Two validators require producer-order repair: the proposed 352-byte unit and the historical duplicate child counter at `utility-child-arm7-wram:ARM037FDDCC/76`. Host02 had already passed in X; its publisher regenerates indirectly, and its Root-specific old object names must not be treated as X's current input names. The remaining channel-parameter paths belong to the validator's deliberately invalid object-window control, created inside its own main routine around lines 196–217. Their absence before that control is expected.

`replay_arm7_child_counter_clean_20261031.py` applies the same output-only routing and producer-first replay to that existing duplicate proof. It preserves the original matcher, validator, profile, native oracle, C and header. Historical report hashes differ between the lane and integrator because the reports retain their original build metadata; both exact known variants are pinned, and the selected bytes must remain unchanged throughout one replay. Every full proof retains 2,048 actual outer returns and 4,096 separate nested returns. Its 36 original controls and four fresh-output/cache controls remain required. The duplicate contributes zero additional functions or bytes.

This audit is a triage aid. It does not prove correct execution order merely because a producer is registered. Computed imports, indirect checks and computed report names remain outside its recognized static scope. Root's 137 and X's 129 oracles without recognized direct product checks are explicitly reported as such. Reports over 8 MiB are withheld for targeted review; none required withholding in these two final scans. Source and native execution gates remain responsible for acceptance.

The initial audit retained complete parsed reports and reached a 5,364,617,216-byte working set. Only its confirmed owned process was stopped. Its raw script and failure receipt are preserved. The final audit retains compact facts, skips reports without recognized direct product gates and completed each real registry scan in seconds. X, Y and the integrator's source, registry and products were read only throughout this work.

## Reproduction

From any working directory, invoke the repository's explicit Python 3.13.5 executable and either wrapper by absolute script path. No work argument is required; each creates a fresh output directory.

```powershell
& C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe C:\Users\trevo\Documents\RecProgramming\DQM\j2p-recovery-lanes\arm7\replay_arm7_seq_main_proposed_clean_20261031.py
& C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe C:\Users\trevo\Documents\RecProgramming\DQM\j2p-recovery-lanes\arm7\replay_arm7_child_counter_clean_20261031.py
```

The standalone auditor takes explicit `--repository`, `--cold-checkout` and optional `--output` paths. It never runs an external producer or writes to either inspected repository. Root owns replacing the two oracle commands after its active frozen cohort terminates. All work in this note has zero new reconstructed-source, native-byte or whole-ROM credit.
