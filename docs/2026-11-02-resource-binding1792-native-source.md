# Resource setup and material binding — 2026-11-02

Six main ARM functions reconstruct 1,792 initialized bytes in ordinary C:

| Address | Bytes | Bounded measured role |
| --- | ---: | --- |
| 02031FA4 | 568 | Resource signature dispatch, allocation transaction, rollback and binding |
| 0202F3DC | 176 | Iterate model dictionary and combine texture/palette binding results |
| 0202EFE4 | 256 | Resolve texture names, skip existing bindings, update binding result |
| 0202F250 | 264 | Resolve palette names, skip existing bindings, update binding result |
| 0202EDFC | 304 | Apply texture parameters and fixed-point magnification to indexed materials |
| 0202F170 | 224 | Apply palette base conversion to indexed materials |

Every final source unit passes the unchanged normal MW linker against its entire measured span. The two internal helpers previously failed because their source symbols were local. Ordinary C visibility promotion and separate helper declarations resolve that failure without changing linker policy, encoded instructions or source boundaries. SDK types use explicit 32-bit scalar aliases. Complete original enum declarations remain intact. An unrelated ambiguous SDK callback alias is excluded and asserted unused rather than assigned a guessed address.

The five binding units use the v3 source directory. Setup uses v4: direct pointer/result casts and the selected raw callees' explicit signatures. This preserves its 568 exact bytes while resolving a selected palette setter's raw pointer return through an explicit discard. The earlier inline-view setup also compiled to 568 bytes but matched only 519; that variant remains a failure and is not selected. Historical generation, symbol-kind and mutation-selector failures are retained. No SDK revision is asserted to be the game's original source revision.

`python match_main_resource_binding1792_20261102.py` installs all six compiled bodies together. There are 2,048 binding pairs and 2,304 setup pairs: 8,704 actual original/source top returns. Each run starts on a fresh ARM946 machine. Registers, flags, guarded stack, all initialized main/input bytes, ordered reads/writes and hardware observations agree. Independent models check names and missing-name results, bound flags, repeated material indices, texture format/key selection, magnification rounding, palette conversion, allocation argument order, zero sizes, every failure combination, rollback and successful binding. Setup's return intentionally ignores a model-set binding failure, matching native behavior.

Binding executes original dictionary lookup and fixed-point division, with no function providers. The divider model supplies 3,784 paired positive-operand operations using the pinned SDK mode/register and rounding definitions. Immediate results do not prove physical timing, interrupts, negative operands or divide errors. Setup supplies four allocation/free callbacks and two upload services, with 3,136 paired backend calls kept separate from actual public returns. Those services record typed arguments, return controlled words and clobber caller-saved registers/flags. They intentionally have no game-RAM effects. This tests the transaction caller, not native VRAM allocation, texture upload or rendering. Zero-size successful branches can free key zero when another allocation fails; free return values are ignored by the measured caller.

The corpus observes 1,720 code bytes and 32 generated pool bytes. All 536 setup instruction bytes and its pool execute, including three initially unvisited default-signature branches reached by nearby invalid signatures. Ten defensive words in the binding routines remain unvisited under valid dictionary/index inputs; their 40 bytes link exactly. Null/invalid dictionary fallbacks that subsequently dereference invalid records are outside the returning corpus. This is not complete malformed-resource validation.

Five whole wrong-C controls produce 6,072 actual returns. Texture XOR, palette XOR, missing-texture success, wrong allocation-format bit and wrong success return reject 229, 181, 124, 112 and 1,108 independent models respectively. Unaffected positives remain explicit. A one-instruction prefix is refused as no return. The boundary audit scans 13,614 configured ARM/Thumb spans, finds ten external direct entry candidates and no interior target/start. Indirect references remain unproved. A read-only selected-source scan finds no named accepted caller into this family before adoption.

Synthetic resources have fewer than 16 dictionary entries, at most three models/materials/bindings and positive original dimensions. Data sizes, pointer targets and initialized records are bounded. Header parsing behavior does not imply game asset validity. Original lookup, division, getters, key setters, callbacks and data receive no additional source credit. Canonical and actual parent-directory Python -I -S reports must match before admission; full module/regression acceptance follows. Windows execution of this group, whole source-only ROM, a full native game and Android device execution remain unproved.
