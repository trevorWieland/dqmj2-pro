# Contributing

## Coordination

Use CLI tools and scripts. Coordinate disjoint ownership by program, CPU, module, mode and address
range; overlapping overlay addresses are not interchangeable. One coordinator owns shared source
selection, module integration and acceptance publication.

Claim a public work-chunk issue before starting. Give the program, CPU, module, ARM/Thumb mode,
address range and intended source paths; recheck for concurrent claims. An open claim remains
active until its owner releases it. Choose another range if ownership overlaps. After a
contribution, record the commit, measured results, limitations and remaining ranges on the issue.
Only the coordinator closes a chunk after its complete scope passes shared acceptance.

## Honest reconstruction

Before changing code, identify the measured original extent, incoming/outgoing bindings, consumed
types, compiler profile and existing ownership. Recover ordinary logic in matching C/C++; justify
assembly only for measured low-level contracts. Never promote decompiler drafts, guessed field
meanings, community names or binary scaffolding to source reconstruction. Keep overlays separate
even when their load addresses overlap.

The only valid evidence is code that compiles and compares. A description of a match is not a
match, and a compile-only pass is not a comparison. Every accepted source change must compile,
pass byte and relocation comparison plus bounded behavioral checks, link all affected modules and
preserve earlier accepted matches. State which checks could not run. Never mark a nonmatching
draft complete, and never hide a mismatch with binary patches, imported original bodies,
arbitrary register constraints or open-ended flag searches.

**Compiler selection is evidence, not a knob.** When a row reproduces only under a build other
than the project's pinned compiler, that is a finding to record, not a reason to move the global
pin: sweep every installed build, promote the row to the *lowest* exact build with a row-level
`compilerSha256` rule in `config/source_units.json`, prove it through the real build path
(`public_tools/repo_build.py`), and only then patch the ledger. Never change
`config/source_units.json:compiler` to fix one row, and never report a permuter score as
acceptance — see `docs/authoring/permuter.md`.

## Comments and naming

Authored code may and should carry concise comments that explain mechanism and intent: why a
range is read, what a packed field means, which hardware or ABI contract a call follows, and where
a measured assumption is uncertain. Comment the non-obvious; do not narrate the obvious. Comments
are part of the code and must stay true when the code changes.

Use meaningful names for functions, parameters and locals. Newly authored code must not introduce
`func_XXXXXXXX`-style names where the mechanism is understood; name a routine by its observable
behaviour or role. Where a contract is still unknown, keep the canonical address identity and say
so in a comment instead of inventing a plausible game meaning.

Keep every formatted authored code file within 500 physical lines as guidance. If splitting a file
to satisfy the limit would make the code harder to read, prefer readability and explain the choice
in review. Match neighboring formatting and do not reformat unrelated source.

## Documentation

Documentation belongs in comments next to the code, and in `docs/` only when it describes
cross-cutting design that no single file can explain. Do not create per-packet evidence documents,
acceptance receipts, manifest summaries or progress write-ups. Prose that restates a diff is stale
as soon as the diff changes; a comment in the code moves with the code.

## Progress

Progress is computed by CI from a real build and comparison. Contributors must not commit progress
percentages, manifests of accepted functions, evidence files or claims that the build passes. The
workflow publishes what the checked-out code actually compiles and compares to; hand-maintained
numbers and receipts are not a source of truth. Do not hand-edit or invent progress figures.

## Private inputs

Original ROMs and saves are private only: never commit, upload or reshare them. The same applies
to extracted original payloads, compiler binaries and credentials. Private target inputs must be
recreated from the contributor's own measured ROM. Generated build products, logs and dependency
trees are not committed either.

## Pull requests

A pull request lists the exact reproduction commands and tool identities, the affected functions
and ranges, byte and relocation results, link results, behavioral and negative controls, and
unsupported cases. Keep changes focused on one coherent family. A ByteMatch percentage does not
replace module, regression and behavioral gates.

Put experiments and copied-root replays beneath `work/`. Preserve immutable proof inputs and prune
completed disposable copies after checking live processes and runtime dependencies. Do not create
sibling copies of the repository.
