# Returning SYS10 with original metadata, 2026-10-29

A separate, expanded synthetic metadata context lets the unmodified SYS10 wrapper actually return after creating an actor. Fresh native-versus-linked-C execution passes 28 cases per implementation, 56 actual returns total, with separately initialized machines. This follow-up gives zero duplicate source credit to the previously reconstructed 696-byte constructor/transform pair. It preserves the four earlier `02210CE8` failures and does not use their post-fault state as proof.

Run from any working directory:

```text
python C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\evidence\encounter\actor_metadata_context_20261029.py
```

The fresh replay passed from the parent DQM directory. Generator SHA-256 is `3c2dcf0cd6e0484a2382c64cbde2aacda1215a2990aff20807e0d6b2451842cb`; report `evidence/encounter/actor-metadata-context-20261029.json` SHA-256 is `674dc53ced01c467ee2c8296f39cad03170a5fed5bbea28ae8408f9206d2bd85`. The generator pins and invokes the frozen 696-byte verifier, checks its source/header closure, and compiles and genuinely links fresh bodies in a separate work directory. No previous source, verifier, report or link snapshot is changed.

## Additional measured context

The former fault at ov000 ARM `02210CE8` reads byte `+0x61` from a record returned by main ARM `020449D4`. That getter computes `base + index*100`, using manager `020F69EC+4`. Main loader `02044998` names the original file `EnmyKindTbl.bin` and adds its eight-byte header to establish the record base. This getter was already reconstructed in `main-runtime08`; it receives no duplicate credit.

The file is 51,208 bytes, with EKT header count 512 and 100-byte records, SHA-256 `0b7d0873c3488891b2b65e0f84bfd35b0d23204759a8d40b2cf52165f50f7aab`. Both it and `FldEnmyPrm2.bin` are checked byte-for-byte against the pinned ROM's file allocation ranges. The expanded fixture maps the unchanged kind file at synthetic `026D0000` and sets `020F69EC+4=026D0008`, with its handle word zero. Original field-file, manager and cache setup follows the preserved constructor fixture.

The fixture also initializes the original first 1,399 compact entries at `021D588C`, using the measured loader transformation `(record.u16_at0 &0xFFF) | ((record.u8_at4 &15)<<12)`. The remaining 22 entries are verified zero and remain outside this initialization. The initializers and real file loaders are not executed: these are explicit manually prepared data contexts, without function stubs or asserted real handles. The original bound of 1,399 is not increased to the modified file count 1,421.

Main ARM `020C58C0` retrieves the low twelve bits of this lookup and supplies the index to `020449D4`. The observed working file-oriented mappings are:

| Native field-record ID | Native kind-record index | Kind byte `+0x61` |
| --- | --- | --- |
| 0 | 0 | 0 |
| 21 | 154 | 10 |
| 42 | 292 | 14 |
| 117 | 0 | 0 |
| 770 | 164 | 8 |
| 771 | 6 | 1 |
| 1398 | 182 | 8 |

These are qualified table relationships, without assigning byte `+0x61` a gameplay meaning or equating either ID space with application catalog IDs.

## Actual returns and limits

Each listed field ID executes through SYS10 in all four VM threads. The cases select first-free actor slots 0, 1, 17 and 47, preserve the ninth VM argument `123.5`, clear the earlier output arguments except the returned slot, and independently check the complete created actor record. Native ID 42 in thread 0 returns after 42,199 instructions; the largest observed case uses 42,645. Each call has a 100,000-instruction cap and one-second timeout, requires the actual return sentinel and preserved SP/R4-R11, and reaches the previously failing `02210CE8` instruction successfully.

Freshly linked constructor/transform bodies and unmodified native execution agree on all general registers/CPSR, ordered CPU stores, persistent and VM state, complete actor pool, actor global state, field manager/cache and metadata images. The additional kind manager, kind image and compact lookup are also checked unchanged. Native callees execute without stubs. The separate source build and link directory is `work/encounter-recovery/20261029/replay-actor-metadata-context/`.

This proves returning behavior for the stated manually initialized metadata cases. It does not prove startup/file-loader execution, valid file handles, the last 22 compact entries, malformed metadata handling, a live scene, rendering, collision, travel, save-bank selection, script reachability, encounter access or renewability. Earlier failures remain correct for their smaller contexts; no return or post-state credit is retroactively assigned to them.
