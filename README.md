# Dragon Quest Monsters: Joker 2 Professional

[![Progress](https://bytematch.dev/trevorWieland/dqmj2-pro.svg)](https://bytematch.dev/trevorWieland/dqmj2-pro)

An in-progress reconstruction into readable C/C++, with justified assembly for measured low-level routines. The target is a reproducible ROM matching the measured input exactly.

This repository contains the actual reconstruction sources, headers, DS configuration, compiler profiles and CLI tooling. Supply your own original inputs and pinned compiler; original ROMs, saves, extracted executable/data payloads and binary build products are not distributed.

The initial public checkpoint covers **11,482 accepted functions and 1,224,354 initialized module bytes: 48.727870% of 2,512,636 bytes**. This is native initialized-source coverage, not overall game completion. The measured input is a modified `B2JJ` build with SHA-256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`; equivalence to a clean retail ROM has not been established.

An exact 175,959,612-byte ROM has been reconstructed locally using accepted source together with remaining original executable scaffolding. **A complete source-only ROM, full clean replay and complete native Windows/Android execution remain unproven.**

## Sources and checks

- `src/`: reconstruction sources and authored headers, including selected implementations and prepared work. Inclusion here alone does not grant acceptance.
- `public/accepted-functions.json`: the closed checkpoint's selected function identities, source/include hashes, compiler hashes and flags, namespace, dependencies and proof states.
- `public/accepted-data.json`: separately measured data and storage records. BSS does not increase the initialized-byte percentage.
- `config/`: ARM9 sections, symbols, relocations and overlay configuration. ARM7 and embedded-program mappings are handled by the reconstruction scripts.
- `public_tools/`: standalone source-integrity and compilation checks; see [public build instructions](docs/public-build.md).
- Root Python scripts: extraction, reconstruction, compiler interfaces, genuine linking, bounded original/source comparisons and regression machinery. Binary tools are pinned in `tools.lock.json`.
- `docs/`: research and historical execution records, including explicit failures and unsupported cases. Historical references to private-only operation are superseded by the [publication policy](docs/public-reconstruction-policy.md).

The public source checkpoint starts a clean Git history. Its manifest preserves exact source hashes from the local closed cohort 172, source revision `efe36ed2e7d16be9f2aae411f0dc0cb3eb89e6d5`, closure revision `14ac8dcd6f8ab0009e5dd54d73cf31c928540776`. Those local historical revisions and generated proof dumps are not included as public ancestors.

Public CI checks declared source integrity without original inputs. The standalone compiler path recompiles actual sources with the declared compiler profiles; compilation alone does not establish a native match. Full original/source and ROM comparisons require owned inputs in a trusted local environment. Historical validation scripts also depend on generated evidence that is excluded from this initial source export; a fresh full public-checkout replay is not yet established.

## Contributing

Claim a disjoint program/CPU/module/mode/address family before starting. Preserve accepted source and include hashes. Submit readable code, measured interfaces, compiler context, complete function boundaries, genuine byte/relocation checks and bounded behavior evidence. A matching local object becomes accepted only after shared module, regression and committed-input checks pass. Prepared and partially matching regions receive no accepted-byte credit.

Names and game-level understanding are separate work. Investigate callers, callees, tables, strings and consumed layouts; record uncertainty instead of inventing meanings. See [semantic investigation](docs/semantic-understanding.md) and [contribution guidance](CONTRIBUTING.md).

The public collaboration model draws on [pokebw2](https://github.com/fuddlesworth/pokebw2): real source and configuration, owned ROM inputs, measured reconstruction, and later naming/documentation work. See the [ByteMatch build and report setup](docs/bytematch.md) for the private-input CI, full native-image report scope and registration steps. No pilot percentage or scaffold match is presented as full project completion.
