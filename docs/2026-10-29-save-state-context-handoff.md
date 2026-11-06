# Serialized state and isolated application context, 2026-10-29

The saved numeric and flag planes are present in native deserialization and the application's constructed-record context. The initial `j2p-battle/runtime.py` copy stops immediately before those planes. This is a measured initialization difference. Its effect on a particular battle, route or encounter requires that caller's execution and scenario setup to be checked.

Reproduce with `python evidence/save/state_context_20261029.py`, or invoke the absolute script path from another working directory. Generated evidence is `evidence/save/state-context-20261029.json`. It records the ROM/save hashes, original decoded ARM9 identity, extracted main-module identity, canonical source/object identities, application file hashes, exact function boundaries, signatures, vectors and module-qualified callers. Application sources were read only; no adapter, UI or input was edited. This work adds **zero matched functions and zero matched bytes**. The 436-byte flag and 180-byte counter alternatives repeat frozen `src/save_accessors.c` coverage and provide additional edge evidence only; see `evidence/save/20261029-accessor-reuse-audit.json`.

## Save-to-RAM mapping

Offsets below are relative to the selected serialized bank. To address the second physical image in the captured save, add its separately measured bank offset `0x7100`; the secondary bit plane below is unrelated to that image selection. All four pointer getters and the deserializer are ARM9 `main`, ARM mode.

| Getter | Serialized interval, end exclusive | RAM destination | Bytes |
| --- | --- | --- | ---: |
| `02063AB0`, 12 bytes | `0090..3A68` | `021BD51C` | 14,808 |
| `02063E8C`, 12 bytes | `3A68..3A9C` | `021B9EB4` | 52 |
| `02063F48`, 12 bytes | `3A9C..5D40` | `021BB278` | 8,868 |
| `02063F6C`, 12 bytes | `5D40..70D0` | `021B9EE8` | 5,008 |

Native `save_deserialize` at `0207E160`, 132 bytes, copies these four intervals. For a main-state RAM address `a`, the serialized bank byte is `0x90 + a - 0x021BD51C`. This relation locates the following fields without assigning quest or gameplay meanings.

| State | RAM base | Bank interval | Entry points and complete byte sizes |
| --- | --- | --- | --- |
| Numeric bytes | `021C0DC8` | `393C..3994` | get `02063B18`/16; replace `02063B28`/24 |
| Primary bits | `021C0E20` | `3994..3A54` | get `02063B40`/32; replace `02063B60`/92 |
| Secondary bits | `021C0EE0` | `3A54..3A68` | get `02063BBC`/32; coupled replace `02063C00`/148 |
| Offset-64 view of secondary | `021C0EE8` | `3A5C..3A68`, within the serialized view | get `02063BDC`/36; replace `02063C94`/96 |

Numeric get/replace signatures are `u32 f(int index)` and `u32 f(int index, u32 value)`. Replacement stores the low byte and returns the prior unsigned byte. Bit get/replace signatures are `u32 f(int index)` and `u32 f(int index, int value)`; replacement returns the prior selected bit and treats any nonzero value as setting. Primary bit `i` is byte `0x3994 + i/8`, bit `i%8`. Secondary base bit `i` is byte `0x3A54 + i/8`; its offset-64 view uses `i+64`. These are serialized capacities, not verified legal script-index bounds.

## Initial application context

Read-only AST inspection verifies that `Runtime.__init__` writes `save[0x90:0x393C]` to `021BD51C`. This is 14,508 bytes. It ends at `021C0DC8`, omitting exactly 300 main-state bytes: 88 numeric bytes, 192 primary-bit bytes and 20 secondary-bit bytes. The original decoded ARM9 is 961,560 bytes, SHA-256 `3fa5b22cb337337c606da0bc22bdf298af1e17c03a6b8f31480cddcd5b681d02`; the saved-state regions lie beyond that loaded module. The Runtime overlay begins above these regions. Thus the omitted regions start zero in this isolated initial context.

The captured save contains 40 nonzero numeric entries, 703 set primary bits and 51 set secondary bits. The generated report retains their raw indices with no semantic labels. Those values are absent from the initial partial-copy context. This does not establish that every current battle request reads them.

`NativeRecordReplay.__init__` in `constructed.py` calls the four native getters and copies the complete intervals above. Its `install_into_battle` later copies all four reconstructed RAM sections into the battle runtime. Scenario adapters also deliberately create battle objects, choose seeds and clear battle-context fields. Initial Runtime state, constructed state and an intentionally configured battle scenario therefore need separate evidence. An application should record which context its predicate or scenario used before presenting a result as dependent on the immutable saved flags. This handoff makes no application changes.

The specific `battle_flags_address` expression reads ARM9 literal word `02044450` (`020F69C4`) and adds `20`, yielding `020F69E4`. That address is outside the serialized state planes. Explicit scenario clearing of this battle-context word does not restore the omitted saved primary/secondary state. Its arithmetic is independently reproducible from the pinned decoded executable and read-only Runtime source.

## Coupled transitions and counters

For secondary setter `02063C00`, a base bit changing from zero to any nonzero request sets both secondary bit `i+64` and primary bit 76. Primary76 is bank byte `399D`, bit 4. Clearing the base bit preserves both coupled bits. Clearing primary76 and rearming the base sets primary76 again even if the offset-64 bit was already set. The offset-64 getter aliases the base getter at `i+64`. These rules establish neither a save-bank selector nor a once-ever encounter limit.

Fresh serialized-state transition vectors cover raw indices 0, 14, 15, 17, 19, 63 and 95. Each performs set, clear, primary76 clear and noncanonical nonzero rearm. Native and compiled accessor engines produce identical prior values, state triples and ordered writes. Index95 is a bounded serialized-capacity probe, not a gameplay-ID assertion. The earlier full transition oracle supplies 3,494 cases and 6,988 native/source executions in `mechanics-save-20261029-acquisition-flags.json`.

| Getter / increment, ARM main | RAM halfword | Serialized bank offset |
| --- | --- | --- |
| `02063CF4`/16, `02063D04`/44 | `021BD668` | `01DC` |
| `02063D30`/16, `02063D40`/44 | `021BD66A` | `01DE` |
| `02063D6C`/16, `02063D7C`/44 | `021BD66C` | `01E0` |

Getter signature is `u32 f(void)`; increment is `void f(void)`. Increment first stores a wrapping unsigned halfword, reloads it, and only then stores 9,999 when the reloaded value exceeds 9,999. Initial `FFFF` becomes `0000` with one write; `FFFE` writes `FFFF` then `270F`; initial 9,999 writes 10,000 then 9,999. All three fields are inside both the Runtime partial copy and complete native main-state copy. Fresh serialized-state fixtures cover seven boundary values per field. Earlier exhaustive edge evidence remains in `mechanics-save-20261029-state-counters.json`; gameplay counter names remain unresolved.

## Caller and prerequisite handoff

The generated index contains 116 decoded direct callsites across separate `main`, ITCM and overlay modules. Eighty-five have a locally provable immediate or literal definition for the first argument. Each entry includes module, mode, caller extent/hash, call address/instruction bytes, surrounding instructions, target and any canonical source. Local constant recovery is not a whole-path reachability proof. Indirect script dispatch, tail branches and literal-table classification still require work.

| Caller identity | Measured link | Evidence/useful next boundary |
| --- | --- | --- |
| `main:ARM:0203F9E8`, call `0203FB54` | Primary getter with index86 | Prior helper `0203D10C` must return nonzero before this test; nonzero primary86 contributes bit8 to the result. No story label assigned. |
| `main:ARM:02062904`, calls `02062954/02062960` | Secondary setter indices14/15 | Frozen `saved_reserve_insert_id`: record must exist, must not already occupy reserve, and an empty reserve slot must be found. It stores the ID before both setter calls. This is source-qualified ordering; full gameplay reachability is not re-executed here. |
| `main:ARM:020631D4`, call `02063260` | Secondary setter index0/value1 | Existing inventory path; does not establish once-ever consumption. |
| `main:ARM:02063628`, call `020636CC` | Secondary setter index17/value1 | Native helper `02044CDC` must return1 on this local path. |
| `main:ARM:02066358`, call `02066730` | Secondary setter index19/value1 | Native record/stat update context; remaining path predicates require caller analysis. |
| `main:ARM:0205C288`, call `0205C2A8` | Increment counter at bank01DC | Conditional on native `020653D0` returning zero; frozen source `src/runtime/runtime05/native_main_0205c288.c`. |
| `ov001:ARM:021FB7AC`, call `021FB7F0` | Increment counter at bank01DE | Overlay-qualified identity; no gameplay counter name assigned. |
| `ov000:ARM:0221B070`, call `0221B474` | Increment counter at bank01E0 | Different overlay and load context; no chronology inference. |

A saved predicate needs a selected/validated image, the correct RAM copy, the native index and any caller-specific map/script/resource prerequisites. Existing `evidence/save/static-paths.json` documents explicit normal bank0 loading and separate bank1 recovery. A raw true bit alone does not certify a completed quest, accessible map, active spawn or renewable acquisition opportunity. The companion encounter worker owns predicate and renewability tracing using this common mapping.

## Validation scope

The audit completes 43,460 actual bounded returns: 24 initialization scenarios across original-native and compiled-accessor engines, 21 counter-boundary cases and seven flag-transition cases. Initialization covers the captured save, zero/all-set flag regions and deterministic synthetic state. Synthetic primary sums are recomputed, but this audit does not execute bank validation or claim complete record validity.

Each initialization/counter case/flag sequence starts a fresh Unicorn machine. Registers and stack are reset for every call; return PC, SP and callee-saved registers are checked, and unexpected state writes fail. Native deserialization and its native memory-copy helpers remain original-code providers during this audit. Twelve ordinary C accessor/counter bodies are substituted only after their pinned MW-linked bytes equal the native bytes. No helper scaffolding receives source credit. All selected original decoded ARM9 function bytes are checked against the extracted main-module spans. ROM, save and read-only application hashes are rechecked after execution. No hardware save operation, field-script scheduler, full game or emulator was run.
