# ARM7 pointer routines, 2026-10-29

Five new ordinary C bodies match 180 complete native bytes in the canonical ARM7 WRAM module. They contain no assembly, executable byte arrays, external callee bodies, or linker-generated binding instructions.

| Native ARM address | Complete bytes | Measured operations |
| --- | ---: | --- |
| `0x037FFB1C` | 20 | Clear two words at offsets `0x48` and `0x4C` when the argument is non-null. |
| `0x037FC9A4` | 36 | Append a node using owner offsets `0x6C`/`0x70` and node offsets `0x10`/`0x14`. |
| `0x037FC9C8` | 36 | Reconnect neighboring node fields and replace owner endpoint fields at null boundaries. |
| `0x037FCBA4` | 40 | Update an intrusive backlink and successor backlink, including measured reload behavior under aliases. |
| `0x037FBDBC` | 48 | Extract an owner head pointer and update successor/backlink or empty-tail fields. |

The operation descriptions and list/queue names are structural inferences. They do not establish SDK API types, historical function names, or broader ownership invariants. Native R0 behavior, including the input-register-dependent return in `0x037FCBA4`, is retained without claiming a recovered original C return declaration.

## Reproduction

Run `python verify_arm7_20261029_lists.py`, or invoke the script by absolute path from another working directory. Its frozen source pins cover `src/arm7/20261029rotated27/`. It writes `evidence/matches/arm7-20261029rotated27.json`.

The verifier regenerates the measured canonical runtime boundaries, verifies each C source hash, removes previous mutable compiler outputs, and compiles all five functions with the pinned MW compiler targeting ARM7TDMI. Each complete body must match native bytes without relocations. Every source object is independently split and linked with the pinned `mwldarm` at its measured ARM7 runtime address. Actual linked bytes, symbol address, and symbol size must agree. No original executable object or source-free callee body participates in these isolated links.

The independent model uses sequential word reads/writes, so pointer aliases exercise actual reload and store order rather than assuming a well-formed abstract list. Across 53 pointer geometries, eight deterministic random RAM states, and two return modes, 848 paired native/source cases produce 1,696 actual returning executions. Each execution uses a fresh Unicorn instance. All native instruction addresses are covered in every function's aggregate fixtures.

Checks include complete 4 KiB RAM contents, ordered stores, native R0, preserved R4–R14, and return/CPU modes. R1–R3 and NZCV additionally agree between native and compiled machines; they receive no independent API interpretation. Supported null branches, empty/singleton boundaries, owner/node aliases, self-neighbors, and intrusive backlink aliases are exercised. Arbitrary unmapped root pointers and unaligned pointer fields remain unsupported inputs. Physical hardware and complete module execution are separate checks.

## Discovery and limitations

The private rotation researched 48 previously unmatched small ARM7 candidates with corrected null syntax, measured native scalar widths, register ordering, repaired call prototypes, stack-buffer measurements, and ABI hints. Full byte equality admitted these five; the other 43 remain rejected. Raw draft attempts are `evidence/attempts/arm7-20261029rotated27.json`, with research outputs beneath `work/lowlevel-recovery/20261029-arm7-rotated27/`.

The generic random-register oracle initially lacked pointer graphs and reported unmapped reads/writes. Those failures prompted the dedicated model above; they were not reclassified as successful executions. The final report requires both the fresh compiler/linker gates and every dedicated oracle case to pass before being written.

These matches require integrator registration and accepted module builds before shared coverage counts them. Isolated function links do not establish a whole-module or whole-ROM source build.
