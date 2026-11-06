# ARM7 CARD controls: four complete ordinary-C units

The new host ARM7 WRAM candidates reconstruct 452 initialized bytes: 436 instruction bytes and 16 generated literal bytes. All four source-only builds genuinely link to the measured input bytes. They are pending integrator acceptance, with no whole-module or full-ROM source-completion claim. Existing accepted C, shared declarations, configurations and registries remain unchanged.

| Native ARM entry | Complete extent | C interface | Measured role |
| --- | ---: | --- | --- |
| `03802824` | 60 | `s32 (void)` | Wait first, then reload the argument pointer and return a status predicate |
| `03803094` | 80 | `u32 (void)` | Issue the original ROM operation and forward the complete received word |
| `03803114` | 84 | `void (CardCommonStorage *, callback, void *)` | Set the busy bit and store callback/argument for busy-clear entries |
| `038031D4` | 228 | `void (u32, u32, s32)` | Receive raw tag/data/enable words, update phase/request and wake the selected original thread |

The compiler inputs are the four C files and two headers under `src/arm7/lane_20261031_card_control452/`. `native_card_types.h` is byte-identical to the reviewed 256-byte common-storage and 92-byte argument-storage views in the previous packet. These are reconstructed view extents, not claims about total original object sizes. Protocol reads use explicit volatile lvalues; phase reset/increment stores and measured snapshots preserve the native scheduling. This bounded proof does not certify asynchronous C semantics or a portable Android threading implementation.

Reproduce with Python 3.13.5 from any working directory:

```
python C:/Users/trevo/Documents/RecProgramming/DQM/j2p-recovery-lanes/arm7/match_arm7_lane_card_control_20261031.py
python C:/Users/trevo/Documents/RecProgramming/DQM/j2p-recovery-lanes/arm7/validate_arm7_lane_card_control_20261031.py
python C:/Users/trevo/Documents/RecProgramming/DQM/j2p-recovery-lanes/arm7/prove_arm7_card_control452_negative_returns_20261031.py
python C:/Users/trevo/Documents/RecProgramming/DQM/j2p-recovery-lanes/arm7/audit_arm7_card_control_transport_20261031.py
```

The positive suite has 3,472 qualified scenarios and 6,944 actual original/compiled entry returns, plus 21,120 separately observed normal native-helper returns. Each original and freshly compiled/linked source executes in its own fresh machine. Complete register/CPSR, stack, mapped-memory, reads and ordered writes are compared. Independent models check the owned ordered stores, return values and protocol/wake targets; only the busy-clear begin-task unit has an independent complete nonstack-memory model. Actual original helper effects remain part of the equivalence comparison rather than being classified as presentation or independently modeled in full.

The preflight suite explicitly swaps the common argument pointer during a bounded lower sleep provider, proving that the pointer must be loaded after waiting. Its 32 raw cases cover old/new status values 0, 3, 4 and FFFFFFFF. The ROM-operation suite uses 20 synthetic control/data-ready/received-word profiles, including a bit-12 mask discriminator and full-word high-bit results. The begin-task suite uses 144 busy-clear flag/callback/argument combinations. The receiver suite uses 672 phase/request/tag/data/enable/current-thread contexts, including phase wrap, all requests 0..31, raw malformed values and actual original kernel/CARD/second-thread prerequisites. Scheduling is disabled, and unexpected context save/load is rejected. Invalid pointer values are only stored, without later dereference or validity claims.

All normal supported cases require an actual return; a one-instruction cap remains unsupported with zero return credit. Busy waits, later callback execution, live IRQ/FIFO delivery, cartridge timing, enclosing-game reachability and access/story/save-bank meanings are unsupported. The TI925T Unicorn model is a bounded execution surrogate, not physical ARM7 hardware. No BIOS, emulator, live save, physical I/O or device deployment is involved.

The rejection suite mutates source/metadata/ABI/layout/current products, then compiles four wrong ordinary-C bodies: caching the argument before wait, using the wrong ROM mask, setting a different busy bit and incrementing phase by two. The cached-pointer mutation moves its BL, so the existing strict linker correctly refuses to infer a native binding at that new offset. The first validator incorrectly expected an output after that refusal; its failure is preserved in `evidence/attempts/arm7-card-control452-negative-link-fixture-failure-20261031.json`. The repaired negative-only path preserves the strict refusal and genuinely links the unchanged wrong-C split object using the already verified positive LCF and zero-code anchors in a separate directory. No accepted linker guard, object, addend or instruction is patched. Each resulting wrong body must actually return and independently fail its model.

A separate zero-credit boundary note identifies the four-byte ARM `BX LR` candidate at `03803090` and the original constructor at `03803168` storing its address into `03809700`. There is no demonstrated indirect invocation or callable C ABI. The 108-byte constructor hypothesis therefore remains unregistered after the strict unknown-symbol refusal. Neither this note nor the embedded initialized bytes add denominator or source coverage.

The transport audit records recursive Python/include dependencies and the frozen callback-scope static manifests, with generated Work products rebuilt by the matcher. Artifact hashes and terminal replay outcomes are in the replay receipt and handoff manifest. Original helper code, unchanged data, zero-code anchors and historical drafts receive no new source credit.

Both source-only runs, including the terminal different-working-directory replay, produced canonical SHA-256 `6944b3bf0c7306edeb631f489b63d726a1fd126db18cf3b3d1720ae7721d74a6`. All 44 controls passed (`2b63fd9c6c7c134ba172528aa480bf64bd2425fd9b20f23a439fe882add81fa6`). The additional negative-return producer separately observes all four wrong compiled C entries returning before independent model rejection (`7aa4e11881a62ab1c5d311ae1d848b292469605c38c9b05d891fb4f4a5a52b36`); register it as its own zero-credit oracle after the controls. All packet compiler/proof inputs are now frozen.
