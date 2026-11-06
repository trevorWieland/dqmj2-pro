# State bits and coupled transitions, 2026-10-29

These six alternative ordinary C implementations cover 436 bytes already frozen in `src/save_accessors.c`; they add zero new functions and zero new matched bytes. Their extra transition oracle is retained in `evidence/save/20261029-accessor-reuse-audit.json`. Alternative source is `src/mechanics_save/20261029_acquisition_flags.c`, SHA-256 `990799f96364aa22d6d539b7727cc0fc4c098498893bb37524a2a93ac1be81f1`; object SHA-256 is `38b8c660ab0cc65c225c98db2da63a27198a741b93a29d569e3622cae68ad498`. Individual native/linked span hashes remain in `evidence/matches/mechanics-save-20261029-acquisition-flags.json`.

| Main ARM address | Bytes | Measured role |
| --- | ---: | --- |
| `02063B40` | 32 | Read one bit rooted at `021C0E20` |
| `02063B60` | 92 | Set/clear that bit and return its prior value |
| `02063BBC` | 32 | Read one bit rooted at `021C0EE0` |
| `02063BDC` | 36 | Read that array with bit index offset 64 |
| `02063C00` | 148 | Set/clear the base bit and perform coupled writes on a rising transition |
| `02063C94` | 96 | Set/clear the offset-64 bit and return its prior value |

Run `python match_mechanics_save_20261029_acquisition_flags.py`. Absolute-script replay from `C:/Users/trevo/Documents/Codex` also passes with identical source/object hashes. The unit uses pinned MW2.0/base, ARM946E, O2 space and inline disabled. All six bodies are independently linked by the actual pinned MW linker and then execute together in the isolated oracle. No synthetic function provider or native callee blob participates.

The 3,494 deterministic cases produce 6,988 fresh native/source executions. Every successful case actually returns within 2,000 instructions. All 103 native instruction addresses are visited. Raw indices zero through 63, selected larger boundaries, both initial bit states, canonical/noncanonical full-width nonzero values, repeated transitions and the offset-64 alias relation are tested. An independent model checks prior-bit return values, every changed word, exact state-word write order and nested calls. Native/source comparison also checks the entire 4 KiB state arena, entire 32 KiB stack, registers, CPSR and ordered writes. Escapes, literal-pool execution, unexpected writes and failures to restore registers/SP/CPU mode are rejected.

Setting a previously clear bit through `02063C00` sets its offset-64 bit and primary bit 76 through the actual reconstructed callees. Clearing the base bit leaves those two bits unchanged. A later zero-to-nonzero transition invokes the coupled setters again even when the auxiliary bit was already set. This is a measured rising-edge rule, not proof of a once-ever event. Each setter returns the original selected bit. Any nonzero 32-bit input value requests setting; zero requests clearing.

Primary, library and auxiliary names are address-based source labels. Serialized offsets and initial application context are now independently mapped in [the state-context handoff](2026-10-29-save-state-context-handoff.md). Primary bytes are bank `3994..3A54`; secondary bytes are `3A54..3A68`. Game-facing acquisition meanings and valid game ID limits remain separate inference questions. Tested larger raw indices do not establish valid gameplay IDs. The auxiliary getter at index `i` aliases the base getter at `i+64`; that address relation is not a save-bank selector. Negative indices, signed index overflow and backing-object bounds beyond the disposable region are unsupported. These bit effects establish no persistence timing or concurrent-writer guarantees.

Original ROM/save inputs, accepted source and earlier reports remain unchanged. The integrator owns shared-ledger acceptance and full module/ROM regression.
