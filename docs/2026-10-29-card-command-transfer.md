# Card command registers and transfer preparation, 2026-10-29

Two ordinary C functions match complete native spans through actual pinned MW linking. They handle card command registers and transfer preparation. This command serialization is distinct from game-save record serialization.

The 96-byte main ARM9 ARM span `02010BA8–02010C08` is `src/mechanics_save/20261029_card_command.c`. Source SHA-256 is `b82263a80bb1ec45549baf28fa989c02571b6690b0eef75e41d9d56d9cea3f48`; object SHA-256 is `5381fa304657ca39935c0c3fab449fdc6622d7235ff8a042d3aa14acf0261fa5`; native/linked SHA-256 is `e57151a4c1fd2e4f3e6eb388463604561e764167c00b92b9a0b658b962dc2dd7`. Run `python match_mechanics_save_20261029_card_command.py`. Its current report is `evidence/matches/mechanics-save-20261029-card-command.json`.

The 84-byte main ARM9 ARM span `02010C08–02010C5C` is `src/mechanics_save/20261029_card_transfer.c`. Source SHA-256 is `09d61e89032bcc76bc999fc17782dd251bc633d31d9f7b34693e865fbbdd9d49`; object SHA-256 is `578e657b3e020cc402d5f81b6a196edfbed986b5d5450288bd433703a013d21f`; native/linked SHA-256 is `75ffd6fefe0c04da2e77f4c036219b042ff717b2fa9f6729fef69ea60b83ec7b`. Run `python match_mechanics_save_20261029_card_transfer.py`. Its current report is `evidence/matches/mechanics-save-20261029-card-transfer.json`.

Both use pinned MW2.0/base, ARM946E, O2 space and inline disabled. Complete spans include their literal words. Repository and absolute-script invocation from `C:/Users/trevo/Documents/Codex` pass with identical object identities. Separate logs are in the corresponding `work/mechanics-save/20261029-card-command` and `20261029-card-transfer` directories.

## Mapped-register evidence

The command oracle runs 528 deterministic cases as 1,056 fresh native/source executions. The transfer oracle runs 608 cases as 1,216 fresh executions, including the separately relinked matching 96-byte command source. Every successful execution actually returns within 2,000 instructions. All 22 command instructions and all 17 transfer instructions are visited. Literal pools, undeclared functions and unexpected writes are rejected.

The command helper polls the mapped word at `040001A4` until bit 31 clears under an explicit readiness script. It then writes byte `C0` at `040001A1`, followed by eight bytes at `040001A8–040001AF`: the first and second input words, each in big-endian byte order. Fixtures cover word/byte boundaries, random full-width words and zero through eight busy reads before the ready read. The complete mapped register page, common arena, stack, registers/CPSR, poll words and ordered writes are compared. An independent model checks all register-page contents and exact write order. The leaf has no platform-call provider and leaves its stack contents unchanged.

The transfer helper passes the measured channel, FIFO source `04100010`, destination and length 512 to an explicit DMA-preparation provider at `02009034`. The provider deliberately changes the common source word and the parameter control word. The recovered caller must then read the updated values: its eight command bytes are `B7`, the updated full-width logical source offset in big-endian order and three zero bytes. It finally writes the updated control word to `040001A4`, after the command call. Four channels, full-width source/control boundaries, busy polling and random cases verify the six relevant call/register effects and ten ordered MMIO writes. DMA implementation is not executed.

These are scripted mapped-MMIO observations. No physical card device, DMA operation, cache coherence, IRQ timing or concurrent transfer is established. The void interfaces make no semantic return-value promise, although all architectural results are compared. The matched command dependency earns no duplicate source credit in the transfer report.

## Failed experiment and acceptance limits

An initial transfer draft misread a literal from instruction-style data disassembly as `020E5940`. Direct measured bytes identify `020E5B40`. Correcting the unaccepted symbol and binding yields the complete match without opcode or relocation patches. The 83-of-84-byte diagnostic attempt and exact failed source snapshot remain zero-credit evidence in `evidence/attempts/20261029-card-transfer/results.json`.

Existing accepted sources and earlier frozen reports remain unchanged. The integrator owns shared-ledger acceptance and complete module/ROM regression.
