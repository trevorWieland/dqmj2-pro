# Item predicate recovery and resource clamps, 2026-10-29

Main:ARM02065E44 is a complete1,300-byte ordinary-C candidate for the private measured build. It decides a local item predicate from a saved32-byte block, optional bonus inputs, species/variant, feature bits, item row and optional live entity. This is separate from inventory ownership, purchase cost, menu access, actual item effects and the consuming caller020731AC. No general item-supply or gameplay-reachability claim follows.

Promoted source `src/mechanics_save/20261029_item_eligibility.c` is264 physical lines, SHA-256 `dee20724bcc1c941404dc244b113ce94eec85969a3125ed0eee4be8490b5e514`. All extern interfaces are explicitly declared. Three plain integer work locals are reused across nonoverlapping bonus/resource phases; no assembly, opcode edits, forced spills, fake arguments or artificial wide return are used. Current-resource getters have mutable block pointers because their native implementations can clamp stored fields.

The pinned MW2.0/base compiler with this unit's `-O2 -opt speed` and declared ABI flags produces object SHA-256 `460973cbf5444ee33474688ce0d7f4e8dd388ba648725d3a9a8b9db233fd5b0f`. The complete body equals the native span after the real independently validated MW linker. Linked/native SHA-256 is `7f34dafeb9e820b4e3af34e63a3a15817efedfad2a8cdb8fcdb4fa1766f41c66`. The source file is standalone with no include dependencies; native callees remain explicit module-qualified bindings and gain no source credit here.

## ABI and field contract

The recovered interface returns a32-bit0/1 result and receives seven arguments:

1. Mutable saved block, corresponding to record+0x20 in the tested record context.
2. Optional bonus byte view; null in the supported execution matrix.
3. Species input, fixed to1 in that matrix.
4. Variant input, fixed to0.
5. Pointer to64 feature bytes, neutral zero bits here.
6. Item ID, indexing the real88-byte rows.
7. Optional live entity, null here.

The first four arguments occupy R0..R3; arguments5..7 occupy caller-SP words0/4/8. The new `eligibility_machine_20261029.py` marshals this explicitly. It requires actual return, restored SP and callee-saved registers within200,000 instructions. Fresh machines isolate each native/source execution. Incoming stack-argument writes are recorded separately from persistent state because native code can store parameter copies in that caller-owned argument area.

Native ItemTbl byte+0x28 supplies the kind and byte+0x29 the subtype. Optional bonus reads use signed halfwords+0/+2 and unsigned bytes+0xC/+0xD before six native cap calculations. Those optional-bonus paths are full-byte matched but not independently executed by this matrix.

Native block-based helpers supply two maxima and two signed current values. The predicate also compares signed block halfwords+0/+2/+8/+0xA/+0xC/+0xE with six native cap results, and tests halfword+0x1C against999 for kind12. Kind48 delegates an additional native leaf condition. The exact source contains the complete kind dispatch, including qualified live-entity and scene-specific dependencies. Operational first/second resource names are retained; this note does not derive additional status/ownership labels.

## Mutation during an eligibility check

Current getters main0207C18C and0207C1B8 call their respective maximum calculation, read signed block halfword+4 or+6, and store the maximum in place when the stored signed value is greater. They then return the signed current value bounded by that maximum. Negative malformed halfwords are not repaired by this greater-than clamp.

Thus an eligibility call can repair a resource field even when it rejects the requested item. In the tested saved-record context those writes are record+0x24/+0x26, bank-relative offsets `0x20C + recordIndex*0x84` and `0x20E + recordIndex*0x84`. This is separate from the marker byte+0x33 previously traced through saved/runtime copies and UI predicates; this fixture does not choose a physical save bank.

Four positive-over-max scenarios cover both fields above maximum, signed maximum32767, first-only and second-only overage. The independent model predicts every halfword write and the resulting whole saved region. In this neutral species1/variant0 context, the measured maxima are165 and69. These numbers describe this exact block/feature setup, not species-wide constants. An over-max first field becomes165 before a kind1 equality test rejects a full-resource request. No inventory debit or item-effect write occurs in these vectors.

## Measured predicate domain

The supported corpus contains all253 real ItemTbl rows outside the three scene-specific kind24 rows, across ten block variants. Variants include the captured block, zero currents, exact maxima, small positive currents, cap-equal fields with the999 limit, signed-negative currents with raw marker255, and the four over-max states. Reserved row values are deliberately included as raw table inputs; successful local predicates do not establish legal obtainable items.

For this null-live-entity domain, the native status-area availability control is0. The independently modeled dispatch therefore rejects the kinds requiring a live status context. Kinds1/2 additionally require a nonzero first current value and a nonfull corresponding resource. Kind3 uses subtype-specific signed current/max comparisons. Kinds12..18 use the documented limit/cap checks; kind26 is rejected by this general predicate and is handled by the separate skill-book caller evidence. Other explicit rejected kind groups and default branches are preserved in source and vectors.

Six cap values, four resource values and the kind48 condition are obtained through actual original native leaf calls. The dispatch and clamp comparisons are independently modeled; those leaf formulas are not re-proved here. The corpus requires a valid block, species1/variant0, neutral features, null bonus and null live entity. Arbitrary species/variant/feature sets, nullable-block edge paths, optional bonus/live entities, scene-specific kind24 and ordinary scene construction remain execution-unsupported despite complete linked-byte equality.

## Evidence and replay

`evidence/application/eligibility-exact-fixtures-20261029.json`, SHA-256 `bb0a66b9af21569cc75f3d2933028cd1cee377fa80d1d76b5abd5e8fc26559e3`, contains2,530 cases,5,060 actual predicate returns and61 actual native leaf-control returns:5,121 total. There are zero callee providers. Whole saved-state hashes and exact clamp write logs match. No other non-stack write is accepted. Original ROM/save and application files are unchanged.

The earlier1,296-byte hypothesis remains in `nonmatching/save-core/20261029-preparation/eligibility_typed.c`. Its original1,518-case/3,077-return report `eligibility-fixtures-20261029.json` remains unchanged at SHA-256 `46c57b1f32707669ba6597dc73673149780a3c0404d1e2d61599dfd39939c70f`. Its unchanged-state result is limited to its six within-maximum variants. Pinned compiler/goal and natural source-lifetime experiments remain separate generated attempt reports. No earlier accepted code or frozen record33 reports are edited.

Canonical `evidence/matches/mechanics-save-20261029-item-eligibility.json` has SHA-256 `db36ff271f08045a6062ee6d81df96729c1542f83707f87c8fa3bf50d379953a`. It contains one exact1,300-byte row, full source/object/immutable link identities, native symbol entries measured against declared module/function starts, and separately hashed replay dependencies. The per-unit speed setting is not generalized to other source units.

```powershell
& C:/Users/trevo/AppData/Local/Programs/Python/Python313/python.exe C:/Users/trevo/Documents/RecProgramming/DQM/dqmj2pro-decomp/match_mechanics_save_20261029_item_eligibility.py --source src/mechanics_save/20261029_item_eligibility.c
```

The matcher and underlying exact verifier both accept an explicit repository-relative source path and pin the promoted source hash. The canonical replay also succeeds from the unrelated Codex working directory with the same report hash. These worker reports establish function matching and bounded behavior; coordinator registration, real module reconstruction and whole-ROM gates are independent acceptance stages. The replay scripts do not mutate shared registry or build files.
