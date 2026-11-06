# Interpreted SCR executable inventory — 2026-10-29

The measured ROM contains an interpreted executable backlog separate from the ARM9/ARM7 native modules. This inventory reconciles every FPK member in the 341 script archives previously identified through member zero. It gives no reconstructed-source credit to original SCR bytes, generated CFG records, inventories or opcode listings. Native initialized-module percentages cannot stand for overall game-source completion while this interpreted ordinary logic remains unreconstructed.

Run `python evidence/encounter/script_inventory_20261029.py`. The versioned summary is `evidence/encounter/scripts-inventory-20261029.json`, and its referenced immutable CFG artifacts are under `evidence/encounter/script-cfg-20261029/`. The generator verifies the original ROM hash, FNT/FAT-backed archive bytes, previous member-zero archive/script hashes, the pinned FPK/ASH reader and the original ARM9 module before analysis. It leaves the earlier encounter trace reports and source unchanged.

| Measured item | Count or bytes |
| --- | ---: |
| Known member-zero script archives | 341 |
| Single-member archives | 228 |
| Eight-member archives | 113 |
| FPK member-table identities | 1,132 |
| Distinct stored ranges, summed within archives | 1,132 |
| Distinct decoded script images | 297 |
| Distinct code hashes | 297 |
| Unique code-container bytes | 14,237,108 |
| Syntactically reached record bytes per unique image | 14,132,876 |
| Unreached or opaque container bytes | 104,232 |
| Reached opaque SYS nodes | 121,682 |
| Native-unsupported opcodes reached by this partial CFG | 0 |
| Unresolved CFG failures | 1 |
| Container/hash validation failures | 0 |
| Reconstructed ordinary script-source units/bytes | 0 / 0 |

All member slots within each known archive decode to the same script as that archive's member zero, despite occupying distinct stored ranges. Duplicate archive images reduce the 341 primary script identities to 297 distinct decoded/code images. These are measured byte equalities, not inferred locale names or interchangeable packing behavior. Exact ROM reconstruction must preserve the original member layout and stored representations until an independently validated source/compiler/packer chain replaces them.

Each archive is keyed by ROM hash, filesystem path, archive hash, original ROM interval and member-table hash. Every member records its numeric slot, raw name bytes/hash, archive/ROM offsets, stored length/hash, compression classification, decoded length/hash, entry-table hash and code length/hash. The image records retain all archive/member references and content-addressed CFG provenance. The summary distinguishes unique decoded images, unique code and physical stored ranges to avoid multiplying source coverage through duplicate members.

## CFG scope

The decoded layout is SCR magic, a 4096-byte table of 1024 signed entry offsets, and code beginning at member offset 4100. The inventory preserves every table value, separates negative entries rejected by native start, and follows nonnegative entry roots. Known builtin control flow includes skip-by-encoded-advance, direct/conditional jumps, CALL targets and summarized continuations, conditional forks, counter self/continuation paths and dynamic return/end nodes. Return continuations are stored as a shared possible set; no context-sensitive stack or returnability proof is claimed.

SYS opcode support is measured from the original ARM9 dispatcher table at 0205A68C, with 358 slots and explicit default block 0205BCF0. Recognized SYS records retain opaque native/script effects and only an explicitly unproven encoded continuation. Such calls may redirect or replace scripts, block, fault or depend on external state. The resulting graph is a partial static CFG, not a complete overapproximation of all dynamic control flow. Zero unsupported opcodes in this reached subset does not certify every potential path or every unreached word.

Record extents may include operands or inline payloads. Unreached bytes are explicitly classified as unproven code/data, not discarded as padding or certified non-executable assets. A high syntactic record-coverage fraction does not measure reconstructed logic, guaranteed reachability or complete executable-byte coverage. Every image retains `completeControlFlowCoverageCertified: false` and zero recovered ordinary script source. The generated node listings are evidence data rather than a source draft.

The referenced compact CFG artifacts total 267,582,065 bytes. They are generated, private evidence outputs; their paths, lengths and hashes are recorded so they can be validated or reproduced without treating them as authored program logic.

## Unresolved original jump

The sole unresolved CFG failure is in member zero of `d145.e`, script SHA-256 `461e9fb8051020c664b8cc9a5d3261f1ded04873a92996d8c5b7235bb6fda631`. Its 10,724-byte code interval contains an unconditional jump at PC 10,396 with words `[1036, 12, 10724]`: the target equals the exclusive code end. The inventory retains the out-of-range target as a failure.

Run `python evidence/encounter/script_anomaly_20261029.py` for the separate bounded native corroboration in `evidence/encounter/script-cfg-anomaly-20261029.json`. It performs native initialization and entry setup, manually selects that actual jump instruction, and observes the native dispatcher returning with PC exactly 10,724 and pending cleared. All three native calls truly return. This confirms decoding and unchecked target assignment. It does not execute the prior branch path or the next instruction fetch, prove the edge occurs in a valid scene, establish resource-loader postprocessing/allocated-tail behavior, or certify a hang, crash or safe exit. No bytes are appended or changed to explain it, and `failureResolved` remains false.

## Remaining work

This scope starts from the 341 known member-zero archives and reconciles their complete member tables. It does not yet establish an exhaustive all-ROM search for scripts in other archive families or other member positions. Future executable discovery remains open.

Recovering script source requires readable ordinary logic, verified variable/native-ID bindings and an exact script compilation/packaging chain. One-opcode-per-line transcriptions, raw byte arrays and the current CFG records do not satisfy that requirement. Native interpreter source, interpreted script source, bytecode container coverage and whole-ROM reproduction must remain separate measurements. No Android run, complete encounter-access proof, live outcome label or renewable acquisition certificate follows from this inventory.
