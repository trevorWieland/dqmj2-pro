# ByteMatch

The tracked version is `B2JJ-modified`, the measured modified Dragon Quest Monsters: Joker 2 Professional ROM with SHA-256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`. A clean retail identity has not been established. The public source repository is [trevorWieland/dqmj2-pro](https://github.com/trevorWieland/dqmj2-pro).

## Build inputs and CI

The build follows [pokebw2's separation of public sources and private inputs](https://github.com/fuddlesworth/pokebw2/blob/main/.github/workflows/build.yml). Matching runs on GitHub-hosted Windows runners on pushes to `main`, plus manual dispatch. Pull requests run source integrity and changed-code standards without receiving private inputs.

The private `trevorWieland/dqmj2-pro-inputs` repository holds an immutable multipart archive and separately pinned supplemental reference archives. Its manifest binds the accepted source snapshot, public accepted-manifest hash and every archive part hash. It includes owned originals, pinned tools and the frozen replay metadata required by this custom build. A ROM and compiler alone do not close the historical replay dependencies. The `BUILD_INPUTS_DEPLOY_KEY` secret is a read-only key for this input repository; ByteMatch requires no credential.

The installer refuses traversal, links, conflicting inputs and replacement public source/configuration. Absent `src/**/*.json` files are private replay descriptors; existing public files at those paths cannot be replaced. Private inputs, build logs and objects are excluded from public Git and artifacts. Reusing the archive on a matching checkout preserves identical existing inputs.

`public_tools/build_bytematch.py --native-only` verifies the inputs, recompiles the complete accepted source manifest, and genuinely links all twenty native modules using the pinned compiler, linker and dsd. Every module must equal its original initialized image, and symbol checks must pass. Additional initialized-data, BSS and composition profiles are compiled from their actual frozen sources. Original executable gaps and veneer scaffolding receive zero source credit. The admitted AuthStart function uses its exact scoped extraction rule; source bytes and compiler inputs remain unchanged.

The receipt binds this public Git revision, the accepted manifest, the current compiler report and the three new native-link reports under a dedicated `work/` directory. Source compilation alone never authorizes a report. Historical cached source objects are optional comparison references; missing caches are recorded as unavailable and are never presented as verified or freshly compiled. The native tracking build inherits closed acceptance and semantic-generation qualifications. It does not rerun historical behavioral oracles or claim a fresh full ROM/container build.

Without `--native-only`, the wrapper also runs `reproduce.py` for the checksum-tool prerequisite and executes `run_checks.py --clean`. That full historical path retains its separate workspace-audit handling: every build/oracle stage and source policy must pass, with no recorded external file changes; only old no-remote/unavailable-snapshot conditions may be superseded by the [publication policy](public-reconstruction-policy.md). Other failures block that full-replay path.

## Generated objdiff project

The initial public checkpoint reconciles as follows:

| Measurement | Accepted bytes | Denominator | Percentage |
| --- | ---: | ---: | ---: |
| Native initialized source, closed cohort 172 | 1,224,354 | 2,512,636 | 48.727870% |
| Measured function code, objdiff | 1,115,554 | 2,122,900 | 52.548588% |

The initialized numerator is 1,115,554 function bytes, 108,776 separately accepted initialized-data bytes and 24 qualified alignment bytes. ByteMatch's current page headline uses function-code matching and does not support the combined initialized metric. The native report also measures 108,776 bytes of genuinely compiled and linked typed data. Combined code and data therefore cover 1,224,330 initialized bytes (48.726915%), which rounds to the same 48.73% local milestone. The separately qualified 24-byte linker alignment remains unmatched in objdiff. The separately labeled [native initialized-source badge](../public/native-progress.svg) and [accounting record](../public/native-progress.json) preserve the local milestone without changing objdiff classifications or promoting original data to source credit. Source-integrity CI checks that this record and badge still agree with the closed manifests.

`public_tools/bytematch_project.py` generates `build/B2JJ-modified/objdiff.json`; do not edit that output. It reads the closed public accepted manifest and all three genuine module-link reports, covering 20 native modules and 2,512,636 initialized bytes. Program, CPU and module namespaces keep overlapping overlay and ARM7/ARM9 addresses distinct.

Each credited unit has a folder-based name derived from its source path, an original target object, a source-side object, a repository-relative `metadata.source_path`, and CPU/program progress categories. Completion requires the closed accepted identity, exact source and object hashes, a genuine exact module link and equivalent freshly compiled function bytes and relocation contracts. Compiler debug/path differences are ignored; function or relocation changes fail. Report symbols use the actual C or assembly definition names, so ordinary source linking requires no source edits or mass renaming.

This integration compares final linked image ranges. The generated ELF containers wrap the original bytes and the independently linked source bytes separately; they do not alter instructions, compiler objects or relocations to obtain a match. The source side contains only admitted source ranges. Original scaffold ranges and regenerated linker bridges receive no source credit. BSS and interpreted scripts are outside the initialized native-image denominator.

Measured candidate and accepted functions enter the code budget. Other initialized spans remain explicit objects in an unclassified data budget with zero completion; the exporter does not invent functions for opaque gaps. All initialized bytes remain represented across code and data. ByteMatch's code percentage therefore describes the measured function inventory, and its data budget includes unclassified bytes that may contain further code. Neither is a precise whole-game executable percentage, the accepted initialized-source ledger percentage, or overall game completion. Source data that is not independently admitted by this function-manifest exporter remains uncredited. Do not substitute these figures for the separate accepted accounting.

The behavioral draft ledger supplies `functional.json`. Only explicitly bounded behavior-qualified, nonmatching functions are included, with `medium` confidence; bounded evidence does not prove general functionality. Accepted functions are excluded from this list.

`public_tools/source_aliases.json` pins the two functional drafts' full physical identities, source definitions and include hashes. `public_tools/source_links.py` generates the display-only `include/bytematch_names.h`; it is not included by compiler inputs. An unchanged copy of the overlay draft and its context header is published under `src/nonmatching/` so the viewer can show it. These source links retain empty source baselines and `complete: false`, adding no matching credit.

After the build, CI runs pinned objdiff 3.8.3:

```powershell
tools/objdiff/3.8.3/objdiff-cli.exe report generate --project build/B2JJ-modified -o build/B2JJ-modified/report.json
python public_tools/validate_bytematch_report.py --project build/B2JJ-modified/objdiff.json --report build/B2JJ-modified/report.json
```

Only `report.json` and `functional.json` are uploaded, in `B2JJ-modified_report`. The validator permits the pinned standard report schema and requires the entire initialized denominator. It rejects instruction-rich diff output, missing units, changed source paths and promoted completion flags. Never upload objects, original images, private logs or the old objdiff self-test JSON.

## Local checks

With the private input checkout available:

```powershell
python public_tools/build_bytematch.py --root . --input-bundle private-inputs --native-only
python public_tools/bytematch_project.py --root . --private-root .
tools/objdiff/3.8.3/objdiff-cli.exe report generate --project build/B2JJ-modified -o build/B2JJ-modified/report.json
```

For inspection against existing historical private outputs, add `--diagnostic` and point `--private-root` at that trusted checkout. The export receipt explicitly marks such output unpublishable; CI never uses this flag. A diagnostic report is not current-build proof.

## Registration and source verification

An administrator must [sign into ByteMatch with GitHub and add the project](https://bytematch.dev/docs/getting-started). Set the default branch to `main` and use the `B2JJ-modified_report` artifact. ByteMatch reads successful default-branch push runs. The badge has no data until registration and successful ingestion.

Once the project page shows the CI commit, run the upstream [source-link checker](https://github.com/Veradictus/ByteMatch/blob/master/scripts/check-source-links.py):

```text
python check-source-links.py trevorWieland/dqmj2-pro --version B2JJ-modified --json
```

Record its sampled found/absent/missing counts, commit and scope. An unregistered project or a report that has not been ingested cannot produce a source-link validation result. For future aliases, follow [ByteMatch source linking](https://bytematch.dev/docs/source-linking): generate a names header from the authoritative mapping instead of changing frozen function bodies or adding comments to authored code.

## Data source visibility

The [source visibility inventory](../public/data-source-visibility.json) binds every generated data declaration to the closed accepted-data manifest. Ten mathematical or typed SDK tables are public unchanged C. Forty-six declarations encode complete game assets and stay in the owned private inputs. Their report units retain their actual `generated/*.c` compiler-input paths, so those data source views are unavailable in public Git. Matching completion describes verified compilation and linkage; it does not imply that asset content is public. Standard report artifacts carry metrics and names without asset payloads. Public semantic encoders are linked separately in the inventory; their historical generation qualification is inherited, not rerun by the native tracking build.

The source-definition sidecar also selects 67 exact header/include definitions from the accepted compiler closure, preventing a different SDK copy with the same function name from appearing in the source viewer.
