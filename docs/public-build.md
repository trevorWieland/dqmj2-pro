# Public source build and matching boundaries

The public repository contains reconstruction source, headers, configuration, tools and documentation. Original ROMs and extracted original executable or asset payloads remain private inputs. A successful source compilation is separate from native byte matching, module linking, exact ROM reconstruction and native Windows game execution.

`public/accepted-functions.json` describes the closed accepted source snapshot. Its `revision` identifies the acceptance snapshot; a clean public repository can have a different Git history. The manifest pins source/include hashes, the exact compiler executable hash, original compilation flags and full program/CPU/module/mode/function identities. Its declared initialized-byte totals come from acceptance accounting, not from the checks below. Initialized source data is listed separately in `public/accepted-data.json` and is outside this function compiler verifier's scope.

The matching target is the measured modified B2JJ build identified by the manifest's ROM SHA-256. Compatibility with a clean retail dump has not been established. Supply the exact measured input privately for matching; the repository does not provide a ROM.

## Check source integrity without a ROM

Use Python 3.13.5. The public tools use Python's standard library and do not import the private analysis, emulator or extraction pipeline.

```powershell
python public_tools/verify_sources.py --root . --report build/public-source-integrity.json
python -m unittest discover -s public_tools -p "test_*.py"
```

An absolute `--root` works when invoking the script from another directory. `--manifest` defaults to `public/accepted-functions.json` relative to that root. Report paths are relative to the root and must remain beneath `build/` or `work/`.

The check verifies all declared source/header hashes, accepted/module-linked states, distinct physical namespaces and quoted include closure. It rejects unpinned or escaping includes, private input directories, binary includes and unsupported file-bearing compiler options. Macro-expanded includes require a materialized, declared source closure. This conservative source check does not evaluate preprocessor conditions or certify repository publication safety.

Preserve source bytes during checkout. Normalizing line endings changes the frozen hashes even when a compiler would treat the text equivalently. The public Windows workflow disables automatic Git line-ending conversion for its process; the repository's attributes must preserve the published source bytes as well.

## Compile accepted source on Windows

Provide the measured Windows compiler package locally, including its normal runtime DLLs and any required license configuration. The compiler package remains separate from public source publication. The verifier searches the explicit compiler root for executables whose SHA-256 matches the manifest; it never substitutes a different compiler version.

```powershell
python public_tools/compile_sources.py --root . --compiler-root C:\DQM-tools\mwccarm --jobs 3
```

An explicit license path is also supported:

```powershell
python public_tools/compile_sources.py --root . --compiler-root C:\DQM-tools\mwccarm --license-file C:\DQM-tools\mwccarm\license.dat --jobs 3
```

Without `--license-file`, the tool uses `license.dat` directly beneath the compiler root if present, or leaves the existing compiler environment intact. It does not install tools, edit global PATH, modify license files or download private inputs. Keep the compiler's vendor runtime files together; executable hash checking alone does not certify every installed runtime DLL.

The command first performs the complete source-integrity check. It then compiles each unique source/compiler/flag combination once, with at most three concurrent compiler processes. Existing relative `-i` directories are resolved beneath the explicit public root. Other accepted flags are preserved, including language and ARM/Thumb settings; a source file is not silently moved to a different compiler profile.

For a bounded pilot:

```powershell
python public_tools/compile_sources.py --root . --compiler-root C:\DQM-tools\mwccarm --limit 10 --jobs 1
```

Select one or more exact source paths with repeated `--source src/.../file.c` arguments. A limited run records `fullManifestCompiled: false`. Outputs and the report are written beneath `build/public-source-compile/` unless `--out-dir` selects another directory beneath `build/` or `work/`.

The verifier checks that fresh output is a relocatable little-endian ARM ELF32 object and records its source-generated symbols, instruction modes, sizes and hashes. Existing ledger `symbol` names can be original aliases, so those lookups are diagnostic. If a manifest supplies an explicit `compileSymbol`, its presence and known instruction mode are checked; optional `compiledBytes` and `sourceFunctionSha256` provide stronger source-object contracts. Whole `objectSha256` comparisons are diagnostic because debug and source paths can change the object container.

These outputs are ARM objects compiled by Windows tools. They do not demonstrate a native Windows game build. Compilation does not read the original ROM, execute imported providers, compare native functions, link modules, rerun behavioral models or grant new source credit.

## Full private-input reproduction

Run matching in a separate trusted checkout using owner-supplied originals and the documented pinned tool/dependency setup. The existing pipeline uses `configure.py` inputs such as `--rom`, `--save`, `--dsd`, `--compiler-archive` and `--deps-source`; consult the main reproduction instructions for the exact measured inputs.

The existing checks include:

```powershell
python install_tools.py --verify
python run_checks.py --clean --tools
```

Those commands are the matching/integration pipeline and can write shared build products. Run them only in an isolated reproduction checkout or through the integration coordinator. The public source checks above are intentionally independent of that pipeline. A current full replay must pass its required checks; an earlier receipt or a successful compile-only run does not replace it.

Original-derived objects, module images, raw byte/disassembly evidence and full private build logs belong with private inputs or reproducible private outputs. Where a frozen verifier needs derived evidence, its exact private file must be supplied or regenerated from the measured ROM and checked against its hash. Removing such files from publication is not itself proof that a clean reproduction can regenerate them.

## CI and ByteMatch

The implemented matching path is the default-branch Windows workflow in `.github/workflows/bytematch.yml`, using a read-only private-input deploy key and no ByteMatch token. See [ByteMatch setup](bytematch.md) for the current build driver, full native-image accounting, report validation and source-link checks. The alternatives below describe earlier exploratory paths; they are not additional credentials required by this workflow.

The public `source-integrity.yml` workflow runs on GitHub-hosted Windows runners for pushes and pull requests. It requires no ROM, private runner, compiler archive or repository secret. It verifies source integrity and rejection cases; it does not claim matching.

A matching workflow can follow the split used by [pokebw2](https://github.com/fuddlesworth/pokebw2/blob/main/.github/workflows/build.yml): trusted builds receive private originals, verify modules and ROM identity, and publish only a progress report. Full private logs and build caches must not become public artifacts. Fork pull requests should remain in the ROM-free tier; GitHub does not normally give them repository secrets. GitHub also [warns against public-repository self-hosted runners](https://docs.github.com/en/actions/reference/security/secure-use) that carry private files.

Two practical matching/report paths are available:

1. Build the reviewed public commit on a trusted local Windows machine and upload its inspected report through ByteMatch's project-token API.
2. Execute the same public validation scripts from controlled private CI with private input access, then upload its inspected report for the actual public source commit. Keep orchestration credentials and originals private; the reconstruction source and validation implementation remain public.

Register the real public source repository with ByteMatch. Its source viewer can then resolve repository-relative `source_path` values at the report's public commit. A separate metadata-only mirror is not the publication plan.

Generate genuine objdiff reports privately using original target objects and the accepted source objects for the last closed snapshot. Existing pinned commands include:

```powershell
tools\dsd.exe objdiff --config-path PRIVATE_CONFIG.yaml --output-path PRIVATE_REPORT_DIRECTORY --skip-absent-objects
tools\objdiff\3.8.3\objdiff-cli.exe report generate --project PRIVATE_REPORT_DIRECTORY --output PRIVATE_REPORT_DIRECTORY\report.json --format json
```

The configuration needs an audited source selection: uncredited scaffold objects must not enter the current-source side merely because they exist in a build directory. Preserve unknown/unreconstructed targets, unique host/child CPU/overlay namespaces and zero credit for imported provider bodies. Never upload a one-function pilot as whole-project progress.

Objdiff code/data percentages use different accounting from initialized-module coverage; data totals can include BSS. Do not replace the accepted initialized-byte percentage with an objdiff figure. Do not derive fuzzy matching percentages from the existing byte-comparison counters. `metadata.complete` must reflect real source linking, and the report must retain original targets rather than obtaining an assumed match from a targetless complete unit.

ByteMatch is a presentation layer. The full public source, build configuration and independent validation remain the reproducible evidence. Matching percentages, bounded behavior, semantic understanding, interpreted-source recovery and native platform execution remain separate dimensions.
