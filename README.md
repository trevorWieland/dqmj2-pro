# Dragon Quest Monsters: Joker 2 Professional

[![Progress](https://bytematch.dev/trevorWieland/dqmj2-pro.svg?label=Function%20code)](https://bytematch.dev/trevorWieland/dqmj2-pro) [![Initialized source](public/native-progress.svg)](docs/bytematch.md)

The two badges measure different scopes: ByteMatch shows measured function-code matching; initialized source preserves the closed local code/data/alignment ledger. [See the reconciliation](docs/bytematch.md).

An in-progress reconstruction into readable C/C++, with justified assembly for measured low-level routines. The target is a reproducible ROM matching the measured input exactly.

This repository contains the actual reconstruction sources, headers, DS configuration, compiler profiles and CLI tooling. Supply your own original inputs and pinned compiler; original ROMs, saves, extracted executable/data payloads and binary build products are not distributed.

Closed cohort 176 covers **11,660 accepted functions and 1,267,058 initialized module bytes: 50.427440% of 2,512,636 bytes**. This is native initialized-source coverage, not overall game completion. The measured input is a modified `B2JJ` build with SHA-256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`; equivalence to a clean retail ROM has not been established.

See the [checkpoint 176 qualification and limits](docs/closed-checkpoint-176.md) for the committed proof scope and remaining checks.

An exact 175,959,612-byte ROM has been reconstructed locally using accepted source together with remaining original executable scaffolding. **A complete source-only ROM, full clean replay and complete native Windows/Android execution remain unproven.**

The [native storage subsystem](ports/native-storage/README.md) builds on Windows x64 and Android ARM64. Its Windows host tests and Android link checks pass CI; complete game and Android device execution remain unproven.

The [native resource subsystem](ports/native-resources/README.md) adds NitroFS loading, G3D dictionary lookup and the accepted texture/palette setters. It has standalone synthetic host tests and an Android ARM64 build, with no private inputs required. This subsystem adds no decompilation progress credit.

The [native scene matrix library](ports/native-scene-matrices/README.md) adds checked matrix commands, node poses, static scene events, per-shape snapshots, homogeneous POSITION records and an isolated warm billboard API. Its synthetic Windows tests and Android ARM64 build need no private inputs. These portable components add no decompilation progress credit.

## Sources and checks

- `src/`: reconstruction sources and authored headers, including selected implementations and prepared work. Inclusion here alone does not grant acceptance.
- `config/source_units.json`: the compilation rule for each source directory (module, processor, flags, load base and original image). Merging a source file into an existing directory is the only step needed for it to be compiled and measured; see [source units](docs/source-units.md).
- `public/accepted-functions.json`: historical closed-checkpoint evidence retained for comparison. It is not read by the current build, which enumerates `src/` directly.
- `public/accepted-data.json`: separately measured data and storage records. BSS does not increase the initialized-byte percentage.
- `config/`: ARM9 sections, symbols, relocations and overlay configuration. ARM7 and embedded-program mappings are handled by the reconstruction scripts.
- `public_tools/`: standalone source-integrity and compilation checks; see [public build instructions](docs/public-build.md).
- Root Python scripts: extraction, reconstruction, compiler interfaces, genuine linking, bounded original/source comparisons and regression machinery. Binary tools are pinned in `tools.lock.json`.
- `docs/`: research and historical execution records, including explicit failures and unsupported cases. Historical references to private-only operation are superseded by the [publication policy](docs/public-reconstruction-policy.md).

The public repository began with a clean Git history at closed cohort 172 (source revision `efe36ed2e7d16be9f2aae411f0dc0cb3eb89e6d5`, closure revision `14ac8dcd6f8ab0009e5dd54d73cf31c928540776`). Historical manifests bind the closed checkpoints listed in the docs; they are not the build input. Progress now comes from compiling the current `src/` tree in CI.

Pull-request CI verifies declared source integrity without original inputs. Default-branch CI resolves every `src/` file to a compilation rule, compiles every resolved C source with the pinned compiler, patches each function's ELF relocations against the measured symbol addresses, and reports byte-exact matches against the original module images. A full historical behavioral replay and fresh complete ROM/container build remain separate checks. See [data source visibility](docs/bytematch.md#data-source-visibility) for the public numerical tables and private generated asset declarations.

## Contributing

Claim a disjoint program/CPU/module/mode/address family before starting. Preserve accepted source and include hashes. Submit readable code, measured interfaces, compiler context, complete function boundaries, genuine byte/relocation checks and bounded behavior evidence. A matching local object becomes accepted only after shared module, regression and committed-input checks pass. Prepared and partially matching regions receive no accepted-byte credit.

Names and game-level understanding are separate work. Investigate callers, callees, tables, strings and consumed layouts; record uncertainty instead of inventing meanings. See [semantic investigation](docs/semantic-understanding.md) and [contribution guidance](CONTRIBUTING.md).

The public collaboration model draws on [pokebw2](https://github.com/fuddlesworth/pokebw2): real source and configuration, owned ROM inputs, measured reconstruction, and later naming/documentation work. See the [ByteMatch build and report setup](docs/bytematch.md) for the private-input CI, full native-image report scope and registration steps. No pilot percentage or scaffold match is presented as full project completion.
