# Source units

The build measures the repository, not an acceptance list. `config/source_units.json` describes how to compile each source directory; it does not list functions or completion states. A source file merged into an existing directory is compiled on the next CI run without a second registration step.

## What the configuration contains

| Field | Meaning |
| --- | --- |
| `glob` | `dir/**` for a directory tree or an exact source path for a profile exception. |
| `module` | One of the twenty measured physical modules (`main`, `itcm`, `dtcm`, `ov000`–`ov007`, the ARM7 modules and the embedded utility-child modules). |
| `processor` | `arm9` or `arm7`; must agree with the module inventory. |
| `compilerFlags` | Inline flag array, or the name of an entry in `flagProfiles`. |
| `loadAddressBase` | Runtime load address of the module image. |
| `originalImage` | Extracted module image compared against the compiled bytes. |

`modules` supplies each module's processor, load address, image path and initialized byte count, so a rule normally records only the module and the flag profile. `flagProfiles` de-duplicates the repeated compiler profile text. `compilers` maps each used MW compiler SHA-256 to its repository-relative binary; a rule may select a non-default compiler with `compilerSha256`, because different source waves were accepted with different compiler revisions.

Rules inherit. The effective rule for a path is the merge of every matching rule from the shallowest to the deepest scope; a deeper rule only states the fields it changes. For example:

```json
{"glob": "src/main/**", "module": "main", "compilerFlags": "p000"},
{"glob": "src/runtime/ov006-reuse/**", "module": "ov006", "compilerFlags": "p012"}
```

A file under `src/main` inherits `main`; a file under the second tree overrides the module and the flag profile. Everything else is inherited from the module table.

## Resolution and failure behaviour

`public_tools/source_units.py --root . --check` walks the whole `src/` tree and resolves every file. There is deliberately no `src/**` catch-all. A file that matches no rule fails the CI step with the list of unresolved paths; it is never skipped. `src/nonmatching/**` is the only default exclusion, and it is explicit in the configuration.

## Deriving the rules

`public_tools/derive_source_units.py` is the maintainer recipe. It reads the private `ledger/functions.jsonl` (the measured compiler profile of every accepted address) and `ledger/modules.json` and emits a reviewable rule set. It is not part of the build and is never run in CI.

The derivation chooses the dominant `(module, processor, compilerFlags, compilerSha256)` profile for each source file, then emits directory rules from the root down. A file whose accepted profile differs from its directory rule gets an exact-path override; these are compiler-profile exceptions, not completions. Top-level directories receive a fallback rule so a new subdirectory inherits a complete module/profile.

The generated header records counts only: source files, ledger source files and the number of source files with more than one historical compiler profile. Those multi-profile files are resolved to their dominant profile; the alternative profiles remain historical evidence in the private ledger and are not listed publicly.

## Build and measurement

`public_tools/build_bytematch.py` installs the pinned private inputs, verifies the runtime tool identities, and calls `public_tools/repo_build.py`:

1. Resolve every `src/**/*.c` outside `src/nonmatching/**` to one rule.
2. Compile each file with the pinned MW compiler and the rule's flags. Long Windows paths are mapped through a temporary `subst` drive.
3. Parse each object's functions and relocations. Functions carry their measured address in the symbol name (`native_<module>_<address>` or `native_fn_<address>`).
4. Patch `R_ARM_PC24`, `R_ARM_ABS32`, `R_ARM_MOVW_ABS_NC`, `R_ARM_MOVT_ABS` and Thumb call relocations with the measured symbol addresses.
5. Compare the patched function with the original module image. `complete` is `true` only for an exact, full-size byte match.

A source that does not compile is recorded in `build/repository-compile/report.json` as an unmeasured unit. It receives no credit and does not stop the rest of the tree from being measured; an unresolved rule is fatal. Historical acceptance never promotes a unit.

`public_tools/bytematch_project.py` reads that compile report and builds one objdiff unit per measured address span. Each unit sets `metadata.source_path` to the repository-relative source path and `metadata.complete` from the byte comparison. The whole initialized denominator is covered by `.text`/`.data` units, including unclassified and target-only spans, so the standard objdiff report and `validate_bytematch_report.py` retain their existing scope checks.

## Relationship to the historical manifest

`public/accepted-functions.json` and `public/accepted-data.json` remain historical evidence. The code build no longer reads the function manifest: the compiled set comes from `src/`, and `complete` comes from bytes. `public/accepted-data.json` is still the separately measured initialized-data budget, because data is compared by measured extent rather than compiled function body.
