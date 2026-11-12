# Lane rule fragments: `config/rules.d/`

Status: adopted 2026-11-12. The loader, the duplicate-glob contract, the tests and this document
ship now. No lane fragment ships this round: the demonstration fragments were dropped at rebase
because main already owned those rules.

## Why

Every lane that added a source directory appended a rule to the single `rules` array of
`config/source_units.json`. That file is 4,700 lines and every append lands near the same sorted
position, so every concurrent pair collided. Four consecutive pull requests had to be rebased and
re-verified after they were already green:

| round | PR | lane | conflict |
| --- | ---: | --- | --- |
| ov001 pass 4 | #185 | `codex/ov001-pass4` | `config/source_units.json` rule append |
| ov000 gen1 | #187 | `codex/ov000-gen1` | `config/source_units.json` rule append |
| asm chunk 2 (Thumb half) | #190 | `codex/asm-chunk2` | `config/source_units.json` rule append |
| rules fragments | #191 | `codex/rules-fragments` | `config/source_units.json` after #189 merged |

The cost is not the text conflict. A rebase invalidates the compile comparison and the whole-image
link result, so green work is re-run because two unrelated lanes touched one shared file.

## Design

`config/rules.d/*.json` holds lane-owned rule fragments. Each file is a JSON array of rule objects
with exactly the same shape as an entry in the base `rules` array:

```json
[
 {"glob": "src/verified_assembly/20261112_asm_chunk_scan/ov006/**", "module": "ov006",
  "compilerFlags": "p003",
  "compilerSha256": "89b2fc16c7f1f29ede1e52bdee5bc8ae4d63fe7e50d8074354dfd92c43d47aca"}
]
```

One file per lane, so two lanes never edit the same file. The base `config/source_units.json` keeps
its existing `rules` array unchanged; no migration of older rules is required.

## Resolution order (deterministic)

`public_tools/source_units.py` performs these steps in order:

1. Enumerate `config/rules.d/*.json` and sort by filename (bytewise, case-sensitive). Filesystem
   enumeration order is never used. A missing directory means zero fragments.
2. Read each file as a JSON array and validate every entry with the same `validate_rule` used for
   base rules. A malformed fragment raises `SourceUnitError` naming the file.
3. Merge as **fragments first, base second**: fragment entries in filename order and file order,
   followed by the base `rules` list verbatim.
4. Reject a duplicate glob across the entire merged set. The message names the glob, the file
   declaring it second, and the file that declared it first.
5. Stable-sort the merged list by scope specificity `(slash count, length)` and resolve a file by
   merging every matching rule from shallowest to deepest; later fields override earlier fields.

Consequences:

* **The most specific glob wins**, whether it lives in a fragment or in the base file. A fragment
  rule for `src/foo/bar/**` overrides a base rule for `src/foo/**`; a base rule for
  `src/foo/bar/baz/**` still beats that fragment rule for `baz/`.
* A rule inherits every field it does not state, exactly as before. A fragment usually states only
  `module` and `compilerFlags`, plus `compilerSha256` or `mode` when they differ from the parent.
* Fragment-before-base is the deterministic listing order for diagnostics. It cannot change a
  resolved value: two distinct matching scopes always differ in depth, and a repeated scope is
  rejected as a duplicate.
* `--check` reports `baseRules`, `fragmentFiles` and `fragmentRules` alongside the total
  `configRules`.

## The demonstration migration, dropped at rebase

The first revision of this branch (PR #191, commit `f4a98e19`) moved the three most recent merged
lanes into fragments and proved a byte-identical resolved map. By the time it rebased onto main,
#189 had merged while those lane rules were still in the base file. This revision takes main's
`config/source_units.json` verbatim and deletes no base rule, so the three fragments were dropped
rather than duplicated:

| dropped fragment | rules | globs |
| --- | ---: | --- |
| `config/rules.d/asm-chunk-scan.json` | 6 | `src/verified_assembly/20261112_asm_chunk_scan/{main,ov000,ov001,ov003,ov005,ov006}/**` |
| `config/rules.d/ov000-gen1.json` | 2 | `src/ov000/g1_ov000_gen1/**`, `src/ov000/g1_ov000_gen1/asm/**` |
| `config/rules.d/ov001-pass4.json` | 1 | `src/ov001/p11_ov001_pass4/**` |

`config/source_units.json` is unchanged from main at this revision (3,129 rules) and
`fragmentRules` is 0. The loader is the deliverable; the migration is only a demonstration, and
shipping it after the rebase would have meant deleting rules that main already owns. The next lane
that adds a source directory creates the first real fragment.

## Proof

At zero shipped fragments the tree is identical to main: `config/source_units.json` is
byte-identical to `origin/main`'s copy, and the loader reads `config/rules.d/` as empty (only its
README is present).

The full-tree golden test performs the migration this branch would have shipped, without committing
a fragment: it takes the real base rule `src/main/**`, removes it from a copy of the current merged
rule list, writes it to a temporary `config/rules.d/golden-split.json`, and asserts the resolved
rule is unchanged for every one of the 15,334 non-excluded source files under `src/`. That is the
same relocation the first revision performed for nine rules, and it pins the loader semantics for
the next real fragment.

The earlier revision's real nine-rule move was also proven byte-identical over 15,274 files
(SHA-256 of the resolved map `57272087ee926bf88d2de28b669a74e6f3833ae0109c36ddf3e9de445de45b42`).
It was reverted here only to keep main's base file intact.

End-to-end checks on this tree:

* `python public_tools/source_units.py --root . --check` → `unresolved: 0`; `baseRules: 3129`,
  `fragmentFiles: 0`, `fragmentRules: 0`, `configRules: 3129`.
* `python public_tools/repo_build.py --root . --private-root . --compile-only --jobs 3 --source
  src/verified_assembly/20261112_asm_chunk_scan/ov006/native_ov006_0220692c.c --source
  src/verified_assembly/20261111_main_families/native_main_02000ce8.c --source
  src/main/goal_resume_20261106/controller_second/native_main_02076440.c` → 3 selected, 3 compiled,
  0 failed. No fragment is shipped, so all three resolve through base rules; the ov006 unit still
  resolves to `p003` (`-opt speed`) from its base rule.
* `python public_tools/whole_image_link.py --root . --check-layout` → `layout-ok`; every header
  check agrees.
* `python -m unittest public_tools.test_rules_fragments` → 19 tests pass, including the full-tree
  split-golden test above. `python -m unittest public_tools.test_source_units` → 11 pass.
  `python -m unittest ops.test_form_search` → 25 pass.

## What a future lane does

1. Create exactly one file, `config/rules.d/<lane>.json`, where `<lane>` matches the branch name
   without `codex/` (lower-case kebab-case). Do not edit `config/source_units.json`.
2. Put only your lane's rules in it, as a JSON array. State `glob`, `module` and `compilerFlags`;
   add `compilerSha256` or `mode` only when they differ from the parent rule. State only
   directories the lane adds, not a copy of the inherited parents.
3. Run:

   ```powershell
   python public_tools/source_units.py --root . --check
   python -m unittest public_tools.test_rules_fragments
   python public_tools/repo_build.py --root . --private-root . --compile-only --source <your-lane-source.c>
   ```

4. If the check reports `Duplicate source-unit rule glob`, another lane or the base file already
   declares that scope. Give your directory a distinct glob, or ask the coordinator to move the
   older rule; never work around it by editing the shared base file.
5. Keep the fragment in the same commit as the source it covers. The fragment is the durable lane
   record; the base file is not touched.
