# Dragon Quest Monsters: Joker 2 Professional

[![Progress](https://bytematch.dev/trevorWieland/dqmj2-pro.svg?label=Function%20code)](https://bytematch.dev/trevorWieland/dqmj2-pro) [![Initialized source](public/native-progress.svg)](docs/bytematch.md)

An in-progress reconstruction of DQM: Joker 2 Professional into readable C and reviewed assembly.
The goal is a ROM that reproduces the measured input byte for byte, built from source by the pinned
compiler rather than patched from the original.

The two badges measure different scopes: ByteMatch shows measured function-code matching, the
second badge shows initialized native module bytes. [See the reconciliation](docs/bytematch.md).

## Where it stands

| measure | value | source |
| --- | --- | --- |
| Matched function code | **54.55911%** (1,161,558 of 2,128,990 bytes) | ByteMatch `B2JJ-modified`, commit `597d1c46` |
| Functions matched | **11,717 of 15,308** (76.54%) | same ByteMatch report |
| True backlog | **3,284 rows / 912,134 B** still unmatched | private `ledger/functions.jsonl`, unmatched rows with measured bytes |
| Ledger rows | 16,073 (4,049 unmatched; 765 have no measured size) | same ledger |

**Why the ledger and ByteMatch differ.** The private ledger records **12,024 matched rows**;
ByteMatch measures **11,717 matched functions**. The gap (+307 rows) is merged work that has not
been measured by a published ByteMatch run yet — the ledger updates per accepted row, ByteMatch
only when its build runs. Neither number is wrong; they answer "accepted" versus "measured".

This is native initialized-source coverage, not overall game completion. The measured input is a
modified `B2JJ` build with SHA-256
`674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`; equivalence to a clean retail
ROM has not been established. BSS does not increase the percentage.

**Proven:** an exact 175,959,612-byte container has been reconstructed locally from accepted source
plus remaining original scaffolding, and the ARM7 container and embedded utility images recompose
exactly. **Unproven:** a complete source-only ROM, a clean replay, and native Windows/Android
execution of the full game.

## The five lens artifacts

Each one is a self-contained tool plus docs. Commands run from the repository root; steps marked
*private* need original inputs that are not distributed.

| lens | what it gives you | try it |
| --- | --- | --- |
| **Symbol map** | every measured address → name, size, module, mode | `python ops/symbol_map.py --root <private> --check` (add `--allow-unresolved` to gate on new rows only) |
| **Data dictionary** | proven table layouts with field offsets and confidence | `python public_tools/data_dump.py --root <private> --list` then `--table math_table_0x20d3fe0 --count 8` |
| **Patch tool** | safe ROM edits with header-CRC fix-up | `python ops/mod_patch.py --root . --spec docs/modding/example-title.json --check` |
| **Script VM** | text-VM model, disassembler and assembler | `python public_tools/scr_disasm.py --opcodes`, `python public_tools/scr_asm.py --roundtrip --input listing.txt --image <private image> --offset <n>` |
| **Platform contract** | what a headless port needs, and what blocks it | read [docs/platform/contract.md](docs/platform/contract.md) |

Depth: [docs/data/](docs/data/index.json) · [docs/scripts/vm.md](docs/scripts/vm.md) ·
[docs/platform/contract.md](docs/platform/contract.md) · [docs/modding/](docs/modding/example-title.md).
The full acceptance run over all five is [docs/acceptance/2026-11-11-phase1.md](docs/acceptance/2026-11-11-phase1.md).

## How progress is measured

Default-branch CI resolves every file under `src/` to a compilation rule, compiles it with the
pinned `mwccarm` from `tools.lock.json`, patches each function's relocations against the measured
symbol addresses, and compares the result to the original module images byte for byte. The public
repository contains sources, headers, configuration and tools — **not** ROMs, saves, extracted
payloads, compiler binaries or generated evidence. ByteMatch builds from the same sources against a
private input and publishes the aggregate numbers; no evidence artifacts are committed.

A source that is merged but does not compile to the measured bytes earns nothing. `src/` is a work
area, not a credit ledger.

## Three open decisions

1. **Runtime capture.** Whether to build a RAM-capture harness (`ops/ram_capture.py`) so runtime
   state can be compared, or keep the project purely static.
2. **Compiler generation.** Whether the pinned 2.0/base compiler is the whole answer, or whether a
   per-function compiler matrix should be part of the accepted workflow. `ops/compiler_matrix.py`
   probes this; five representative rows showed 0 of 120 reproductions across installed builds.
3. **Script corpus scope.** The interpreted SCR corpus is 297 images / 14,237,108 bytes with
   measured CFG coverage but no reconstructed source. Whether that is in scope for phase 2 is
   undecided; see [docs/2026-10-29-interpreted-script-inventory.md](docs/2026-10-29-interpreted-script-inventory.md).

## Repository map

- `src/` — reconstruction sources and authored headers.
- `config/source_units.json` and `config/rules.d/*.json` — compilation rules for each source
  directory (module, processor, flags, load base, original image). A new file merged into a directory
  that already has a rule is compiled and measured automatically; a new directory needs a rule. New
  lanes put their rule in their own `config/rules.d/<lane>.json` fragment instead of editing the
  shared base list.
- `public_tools/` — standalone checks and the data/script tools; `ops/` — private-input tooling
  (symbol map, patch tool, disassembly helper).
- `ports/` — native storage, resource and scene-matrix subsystems with synthetic host tests and
  Android ARM64 builds. They add no decompilation credit.
- `docs/` — research records, lens documentation and acceptance reports; start at
  [docs/INDEX.md](docs/INDEX.md).
- Root Python scripts — extraction, reconstruction, compiler interfaces and regression machinery.
  Binary tools are pinned in `tools.lock.json`.

## Contributing

Claim a disjoint program/CPU/module/mode/address family before starting, and grep the whole `src/`
tree for the address first — a duplicate definition costs a review round. Submit readable code,
measured interfaces, compiler context, complete function boundaries, genuine byte/relocation checks
and bounded behavior evidence. See [CONTRIBUTING.md](CONTRIBUTING.md) and
[docs/2026-11-10-code-and-progress-policy.md](docs/2026-11-10-code-and-progress-policy.md).

Names and game-level understanding are separate work: investigate callers, callees, tables and
strings, and record uncertainty instead of inventing meanings
([docs/semantic-understanding.md](docs/semantic-understanding.md)).

The collaboration model draws on [pokebw2](https://github.com/fuddlesworth/pokebw2): real source and
configuration, owned ROM inputs, measured reconstruction, later naming.
