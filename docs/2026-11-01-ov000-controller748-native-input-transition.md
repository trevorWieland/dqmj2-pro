# ov000 controller 748, 2026-11-01

Identity: ROM SHA-256 674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6; ARM9, empty program namespace, ov000 ARM 0x02219494/660. Module SHA-256 783cb72f0d6ee2fdb632aba3e0ae41a9eee0c7e41933192b1680152e50aa61f6.

Readable ordinary C reproduces the complete 660-byte span through fresh pinned compilation and genuine MWLD linking. All 652 instruction bytes are observed across the corpus; two literal words account for the remaining eight bytes. No byte patch or assembly is used. The canonical source is frozen separately from earlier M2C drafts and scheduling experiments.

Reproduce from any working directory:

    python C:/Users/trevo/Documents/RecProgramming/DQM/j2p-recovery-lanes/overlays/match_ov000_controller748_20261101.py

The raw frontend treated a first-component stack load as a cast of the whole 12-byte vector. Native SP+0 loads justify two explicit .x expressions. Three separate component assignments compiled a 664-byte candidate; ordinary whole-vector assignment reproduces the native aggregate load/store and yields all 660 bytes. New signed16 field names at offsets 0x1C/0x1E preserve the demonstrated prefix layout. These are local, instruction-qualified repairs, not a generic unsupported-expression lowering rule.

The independent model covers 218 explicit states: row sentinel byte 0x03, unsigned dimensions, sequential query guards 3/1/2, status and coordinate bytes, signed mode byte, nonzero full-word gates, signed16 offset/cache updates, buttons, a copied/clamped local vector and inclusive +/-0x3000 reference comparisons. Each original/C pair compares every core register, CPSR, complete RAM including stack, ordered nonstack writes and raw register call views. There are 436 actual top returns and 2,186 watched actual native dependency returns. The fixture executes original constant getters 0x02066C3C/0x0202A634, row/index accessors 0x021DF1F0/0x021DF3BC, mode getter/setter 0x020404E0/0x020404F0, flag-byte setter 0x0221993C and the previously qualified 140-byte local-vector clamp 0x02219CE4.

Separately, 1,366 calls use supplied zero-RAM service boundaries: 0x02218800, 0x02041510, 0x02041560, 0x021E7B9C and 0x020418E8. They clobber caller-saved registers/flags, preserving callee-saved registers. These are not counted as native returns. No UI/audio/device activity is invoked. Actual service effects and complete scene behavior remain unresolved.

Three genuinely compiled and private-linked wrong sources actually return and are independently rejected: a strict minimum-width comparison, signed coordinate-byte loading and accepting only secondary gate value one. An initial negative-profile selection reached an earlier buttons branch and did not exercise the mutated secondary guard; its rejected test selection is preserved in dated attempt evidence. The wrong source itself was unchanged when selecting the correct settlement path.

Inputs remain synthetic: state at 0x02245E54 has signed16 offsets 0x10/0x12 and cache 0x1C/0x1E, raw u32 gates 0x20/0x28, reference vector 0x40 and current vector 0x4C. The selected row, unsigned status/coordinate bytes, mode, buttons and every service result are explicitly supplied initial conditions. Setters mutate byte 0x02245E55 and signed-mode storage 0x020F605E through actual native code. No field meaning, current scene state or ordinary input lifecycle is inferred.

All supported signed32 arithmetic is bounded; conversion back to signed16 follows the pinned compiler low16 representation. Wider overflow, aliasing, malformed pointers, untested service effects and host/device behavior are unsupported. Void C preserves every measured physical R0 result without inventing a semantic public return. Parent module/ROM/regression validation is required before source acceptance; helper source receives no duplicate credit. Existing 738/742/750 source and proofs remain unchanged.
