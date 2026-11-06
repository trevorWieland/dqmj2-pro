# Explicit inventory adjustment source - 2026-10-30

This is a zero-new-coverage source-quality alternative for already matched main ARM `020630E4..02063144`, exactly96 bytes. The preserved old primary `src/runtime/runtime05/native_main_020630e4.c` has SHA-256 `ff015a500061220b158304dd69b6588ec69335828692aa123b26a1823aa21959`. Its item/delta interface was present, but its descriptor getter omitted the item and relied on retained hardware R0. Its signed addition could also overflow in abstract C for extreme deltas.

The explicit alternative `src/mechanics_save/20261030_inventory_adjust.c`, SHA-256 `f2828b860f249dadf31b9ccc06c6a214c65a267ab9df22a03f8e97b01f946ee7`, forwards the full signed item word and performs defined unsigned32-bit addition followed by byte conversion. The later signed-byte capacity/floor checks retain the native order. Pinned2base O2 speed and real MW linking reproduce all96 bytes. Object SHA-256 is `66a8e216eb78affd1f3a04755c25ba6714219ddd0df403d68422c9a40de6f448`; native/linked span SHA-256 is `aaee6895472d3c9a78489b45f3d62d7236424ab909bc51d6eac02cd1b0ab5eff`.

Canonical replay:

```powershell
& C:/Users/trevo/AppData/Local/Programs/Python/Python313/python.exe C:/Users/trevo/Documents/RecProgramming/DQM/dqmj2pro-decomp/match_mechanics_save_20261030_inventory_adjust.py
```

The verifier accepts a repository-relative `--source`, checks current complete native bytes, pinned real-link validation, source/object closure and exact acceptance fields, and proposes a hash-qualified primary migration. It does not select a source or register coverage. The canonical report `evidence/matches/mechanics-save-20261030-inventory-adjust.json` has SHA-256 `9ea58c68f623d783fd0f13c9e12598c64174ca15e984bc9b12e449b11853f15d`, identical from repository-root and unrelated working directories.

The independent execution report `evidence/application/inventory-adjust-fixtures-20261030.json`, SHA-256 `be0b8eb6ddfd88013f057184b0319d90653c9caf1b19f910f6773b1e53555613`, has2,408 cases/4,816 original-and-compiled returns, with no callee providers. Its whole-saved-state model includes the native descriptor getter, observed-bit setter, first-insert queues and compaction. Actual return, balanced SP, callee-saved registers, descriptor/RNG invariance and every saved byte are checked on fresh isolated machines.

## Measured arithmetic and side effects

The native order is: read current quantity as signed8-bit; add the full delta; retain the low byte; interpret it as signed8-bit; cap values greater than descriptor byte+0x27; floor negative values to0; call the observation setter; return the final signed-byte quantity. The source preserves this behavior with defined unsigned addition before narrowing. It does not substitute a wide clamp before wrapping.

Synthetic capacities0/1/99/100/127/128/255, quantities0/1/99/127/128/255 and deltas including INT_MIN/INT_MAX are tested. All255 physical descriptors are additionally covered. Upper signed IDs255/256/32767/INT_MAX reject with return0 and no getter, observation or saved writes. The original only checks the upper bound; negative IDs are unchecked and remain unsupported, without an invented lower guard or pointer-safety claim.

Valid IDs always call the original observation setter, including zero quantity or zero delta. The observed bit at `021C0C44 + item/8` becomes set. Previously seen items preserve queues exactly. A first-observed nonzero ID is inserted at the head of its family queue, followed by nonzero values from the old first nine entries, then zero padding. Family is descriptor byte+0x2C equal7 versus other values. Both12-byte queues at `021C0C64` are modeled, including their two reserved tail bytes and the untouched other family.

Item0 sets its observed bit but does not insert a queue entry. Synthetic queues already containing an unseen ID retain duplicates; no deduplication or once-ever acquisition meaning is invented. Empty, hole and dense duplicate-containing patterns are tested independently of arithmetic. These results distinguish observation history from current ownership.

The returned value is final quantity, not the observation setter's return. RNG and descriptor bytes remain unchanged. Original ROM/save, baseline, application, old primary and cohort45 helpers remain unchanged. Source selection belongs to the integrator after identity audit and full module/source/ROM/regression validation, with zero increase in matched function or byte coverage.
