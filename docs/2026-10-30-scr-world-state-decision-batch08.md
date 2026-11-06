# Complete world numeric-state decision source - 2026-10-30

`world.e` entry34 is a complete 1,352-byte function: decoded code `[64268,65620)`, sole private RET65616. It is one substantive source definition and one qualified instance. Eight archive members decode to the same image and do not create eight instances. The remaining 68,376 decoded image bytes, archive representation and native dependencies remain zero-credit scaffolding. No complete-image or whole-ROM reconstruction is claimed.

## Source and measured behavior

The ordinary source is `src/scripts/20261030/batch08/advance_world_state.c`, with `scr_world_state.h` and `world.bindings.json`. The separately versioned restricted C99 backend is `scr_c_compiler_20261030_v6.py`; v1-v5 and previous batches stay frozen. It compiles named getters/setters, explicitly declared module objects, an imperatively reassigned scalar and structured nested `if`/`else`. No source opcode, source PC constant, executable array or per-opcode macro is used. The source-only directory receives three compiler files and the C/header/bindings closure; original bytecode is a comparison input only. Generated output exactly replaces the complete range while preserving the rest of the image.

The function always captures numeric20, numeric28 and primary236. Then:

- Numeric0 equal1 and numeric4 equal15 cause numeric0=2, numeric4=0 and primary8=true.
- Otherwise, numeric0 equal3 permits two independent transitions: numeric4 equal1 causes numeric4=2 and primary8=true; numeric5 equal7 causes numeric5=8.
- Captured numeric20 at least28, primary218 true and a fresh numeric28 equal5 cause primary237=true and primary203=false.

These are raw state identities. No area, story milestone, acquisition eligibility, finite quota or encounter renewability is assigned. Serialized reentry can stop the first numeric transitions after their own writes. A still-true final gate repeats both primary setters even when the stored values already agree; this is not once-ever behavior.

## Storage and type qualifications

`cached_numeric_twenty`, `cached_numeric_twenty_eight` and `cached_primary_236` are explicit `extern` module objects in slots108/109/110. They retain per-module VM state across calls. They are not private automatic variables. Logical scalar storage in this restricted target ABI uses IEEE754 binary32; this is not a claim about native host C boolean object representation. Local `state` uses105; conditional `primary_218` uses106. All 256 words are poisoned and checked after each return, including untouched106 on a false threshold path.

A whole-image audit verifies that every known encoded mode0 index is a canonical finite integral slot0..255, then records every read/write of all five bound slots. All current known references are inside this routine. That absence does not shorten the declared lifetime of108-110 or cover opaque/native/computed accesses. No external direct branch, CALL or entry-table root enters the interior; no shared return tail receives credit.

The new ordered operator is only `>=` on definitely initialized numeric-getter byte provenance. Arbitrary context-float ordering, changed provenance, other ordered operators, uninitialized globals and storage aliases are rejected. Numeric getters provide u8 values; arbitrary-float NaN ordering support is not claimed. Existing equality behavior stays unchanged.

## Execution and acceptance

`python match_scr_world34_20261030_batch08.py` compares the source-only product with current original images and executes original versus rebuilt bytecode in isolated native Unicorn machines. The different-CWD final replay passed 20,352 paired actual native returns, 128 independent machines per implementation, all 4 VM threads, every own instruction, both outcomes at all 8 conditional sites and two complete serialized invocations per scenario. Each native call must actually return within 20,000 instructions / 1,000,000 microseconds. Each SCR invocation has a 96-step bound.

Comparisons include general registers/CPSR, ordered CPU stores, full persistent state and VM state. An independent high-level model verifies ordered setter effects, numeric byte stores, aligned32-bit primary read/modify/write stores, neighboring bits and previous-value results. The complete 256-word register file and retained module objects are checked after each return. Unknown RAM021C0ECC is neither overridden nor assigned semantics; persistent state outside the exact writes stays unchanged.

A separate 176-byte generated ordinary-C control exercises numeric20>=28 for every possible byte value, yielding 3,216 actual native returns. It has zero original-source credit and is separate from the 20,352 paired routine returns. Twelve negative source/profile controls reject before output, covering scope/type/initialization, aliased storage, unsupported comparison/provenance, unknown assignment and out-of-range API values. No additional malformed-native-record support is claimed.

`validate_scr_world34_20261030_batch08.py` validates current source/compiler/header/profile/products, original ROM and archive aliases, full boundaries and module storage references, native API dispatch-case/BL identities, fresh isolated source-only re-emission, every trace/branch/reentry record, the independent full-state model and byte-domain controls. Missing products withhold credit. It returns one `(codeSha256,64268)` record. Root owns shared acceptance and ledgers.

## Existing caller evidence and limits

Frozen `evidence/encounter/guard-paths-20261029.json` contains an actual original synthetic prefix: entry128 at49604, CALL50472 to entry32 at60232, CALL63872 to entry34 at64268, RET65616 to63884, and entry32 RET63968 to50484. Synthetic numeric0/1 are4/0, not an asserted captured-save current-world value. Outer entry128 later faults at an unsupported SYS104 context. Post-fault state is excluded. This historical prefix gets zero outer-entry return credit and zero additional source credit. It proves a caller chain in the supported fixture, not natural scene launch or access/renewability.

An exploratory literal-argument search found primary237 readers in `s10e01.e` and `k01e02.e`, and primary203 readers in nine archive names. They remain work candidates. A reader, nearby native call or filename alone proves neither encounter access nor repeatability.

## Identities and replay

- Original ROM: 175,959,612 bytes, SHA256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`.
- Archive SHA256 `516ee5fa9061712ec2593d8d385ff61e1c3d54c31d3b291246366bfd891e3923`; decoded SCR SHA256 `9c6c4a136b306126a83a8a749df18276aa2a9d328a4add073fc47f50ea0619f8`.
- C SHA256 `a37916359e3cd70b6df1813b7dc1e597f910d6e90691ccca38f81f31d3476259`; header `1925a586fd944285694802df3d149355be853f4a81cadb17828550bf11658b2b`; bindings `ed204331ed62ff1d1ac7a927758f7108607701704463f277cd3e448d576169a5`.
- v6 compiler SHA256 `ea44995cc5d9e13810a3d8f896b830a75b2cd42665a56b26d8289ef39df781a5`; fixture `4dfb558f72ade785f2bc1cb15988f19b56d836943fa49ccef1854c6d0359e304`.
- Python3.13.5 and Unicorn2.1.4. The report pins the remaining closure and records executed argv/CWD.

Run `python match_scr_world34_20261030_batch08.py`, followed by `python validate_scr_world34_20261030_batch08.py`. Absolute invocation from the parent directory is supported. No application adapters/UI, real-save inputs, device deployment or emulator execution were changed or used.
