# Compile-failure recovery: 28 unmeasured source units

Status: fixed 2026-11-12. `repo_build.py --compile-only` now reports
`source-compilation-passed` with 14,544 selected and 14,544 compiled units.

## Symptom

The ByteMatch build reported `source-compilation-partial` with 28 failures classified
`compiler-or-source`. The report is not published while the compile status is partial, so every
source merged in the affected rounds stayed invisible even when its bytes matched.

Reproduction is the full repository compile, not a per-lane probe:

```
python public_tools/repo_build.py --root . --private-root . --compile-only --jobs 8
```

## The 28 units, by cause

| cause | units | mwccarm diagnostic | fix |
| --- | ---: | --- | --- |
| C99 declarations in an arm7 lane compiled with the C90 base profile | 3 | `expression syntax error` / `undefined identifier` on a mid-block declaration | `config/rules.d/compile-fix-20261112.json`: `p014` for `lane_20261031_alarm_registration156/**` and `lane_20261031_card_abi16/**` |
| C99 declarations in main-module runtime, script and WMSP sources | 10 | same | `p049` for the runtime/script directories and `p074` for the two WMSP directories |
| Windows host drivers using `__declspec(dllimport)` / `__stdcall` | 11 | `';' expected`, `identifier '__stdcall' redeclared`, `illegal use of function qualifier(s)` | `src/ports/**` now uses profile `p073`, which adds `-D__stdcall=` and `-D__declspec(x)=`; these files are host harnesses and only their target functions are measured |
| missing quoted header that lives in a sibling lane directory | 2 | `the file '<header>' cannot be opened` | relative includes in the two sources (`../20261101_wl_counter504/…`, `../allocation_detail_text_cursor/…`) |
| long path passed through a stale `subst` drive | 2 (also C99) | `Specified file … not found` / `The filename or extension is too long` | `repo_build.short_paths` now inventories existing substitutions and verifies the new mapping, so it cannot reuse the publish tree's Q:/R:/S: drives |

## Why this surfaced when it did

The files are older than the reporting window: every one exists at `6173f06e` and at
`d24981c7` (the first all-source build). Their rules and contents were not touched by
#195-#200. `git cat-file -e 6173f06e:<path>` succeeds for the failing paths, and compiling
the five files named in the CI report at `6173f06e^` reproduces all five diagnostics.

What changed is the build scope, not the sources. `#87` (`d24981c7`, "Compile every source file
from a committed unit config") replaced manifest-driven selection with repository-wide
compilation and introduced the `source-compilation-partial` status. From that commit onward these
pre-existing non-ledger drafts and host harnesses were compiled on every run; the publication gate
that now treats a partial report as fatal surfaced the condition four rounds ago. `#195` only
changes `-thumb` for assembly sources, and `#196` only adds relocation patching in the measurement
path; neither touches these C compile diagnostics, which is proved by the pre-#195 compile above.

## Verification

```
python public_tools/repo_build.py --root . --private-root . --compile-only --jobs 8
{"status": "source-compilation-passed", "selectedCompilationUnits": 14544,
 "compiledUnits": 14544, "failedUnits": 0, "fullRepositoryCompiled": true}

python public_tools/source_units.py --root . --check
unresolved 0

python -m unittest discover -s public_tools -p 'test_*.py'
Ran 245 tests ... OK

python public_tools/whole_image_link.py --root . --check-layout
{"status": "layout-ok", ...}
```
