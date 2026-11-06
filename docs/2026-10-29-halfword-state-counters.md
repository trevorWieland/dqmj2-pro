# Halfword state counters, 2026-10-29

These six alternative ordinary C implementations cover 180 bytes already frozen in `src/save_accessors.c`; they add zero new functions and zero new matched bytes. Their extra edge oracle is retained in `evidence/save/20261029-accessor-reuse-audit.json`. Alternative source is `src/mechanics_save/20261029_state_counters.c`, SHA-256 `9b8ea24e4a236ffce2d292379c1a0dacf8df76476f01b2245e6ad098c2872db5`; object SHA-256 is `16c98b3593c6592cc688f6d590ed5c04e8486b661389ff0c96bbc19cad83e93d`. Individual native/linked span hashes remain in `evidence/matches/mechanics-save-20261029-state-counters.json`.

| Context offset | Getter address/bytes | Increment address/bytes | RAM halfword |
| --- | --- | --- | --- |
| `4C` | `02063CF4`, 16 | `02063D04`, 44 | `021BD668` |
| `4E` | `02063D30`, 16 | `02063D40`, 44 | `021BD66A` |
| `50` | `02063D6C`, 16 | `02063D7C`, 44 | `021BD66C` |

Run `python match_mechanics_save_20261029_state_counters.py`. Absolute-script replay from `C:/Users/trevo/Documents/Codex` also passes with identical source/object hashes. Source-unit settings are pinned MW2.0/base, ARM946E, O2 space and inline disabled. Every complete function is linked by the actual pinned MW linker. Direct volatile global-field statements preserve the measured load/store order and native register/pool scheduling; no opcode patch or assembly is used. Earlier pointer-local and alignment variants remain zero-credit negative records in `evidence/attempts/20261029-state-counters/index.json`.

The 1,224 deterministic cases produce 2,448 fresh native/source executions. Every case actually returns within 200 instructions. All 36 native instruction addresses are visited. Boundary values around 9,999, the unsigned halfword maximum and sign boundaries are combined with 128 random halfwords per entry and repeated increment sequences. No synthetic function provider or native callee body participates.

Increment first stores the 16-bit wrapped intermediate, reloads that halfword, and writes 9,999 only when the reloaded value exceeds 9,999. This is not an unbounded increment followed by saturation. In particular, initial `FFFF` becomes `0000` in one write; initial `FFFE` first stores `FFFF` and then stores `270F`. Initial 9,998 reaches 9,999 in one write, while initial 9,999 produces the intermediate 10,000 and then clips to 9,999 in two writes.

An independent model checks the exact one-or-two halfword write sequence, resulting field value and unsigned getter result. The complete 4 KiB state page, neighboring fields, unchanged 32 KiB stack, preserved registers/SP/CPU mode, all result registers, CPSR and writes are compared with native execution. Unexpected execution, literal-pool execution, writes outside the explicit field page and timeout fail.

The field labels are measured context offsets. Serialized bank offsets are now independently mapped to `01DC`, `01DE` and `01E0` in [the state-context handoff](2026-10-29-save-state-context-handoff.md). Gameplay meanings and valid gameplay ranges remain separate inference questions. These isolated RAM effects establish no persistence timing, atomicity, concurrent-writer behavior, checksum effect or save-bank chronology. Increment has a void interface; architectural register effects are compared without a semantic return-value promise.

Original ROM/save inputs and existing accepted source remain unchanged. The integrator owns shared-ledger acceptance and complete module/ROM regression.
