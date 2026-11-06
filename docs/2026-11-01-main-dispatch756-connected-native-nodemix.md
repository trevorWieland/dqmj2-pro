# Main dispatcher 756, 2026-11-01

ARM9 main ARM 0x0202F820/72 is reconstructed as ordinary C, including actual table lookup and indirect calls. ROM SHA-256 674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6; main SHA-256 ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f. Fresh pinned O2 space and speed builds both genuinely link all72 bytes. The canonical producer uses speed. All68 instruction bytes are observed, with4 literal bytes.

Reproduce from any working directory:

    python C:/Users/trevo/Documents/RecProgramming/DQM/j2p-recovery-lanes/overlays/match_main_dispatch756_20261101.py

The dispatcher clears u32 state flag mask0x40 before each command, loads an unsigned command byte from the state pointer at offset0x00, selects original table0x020DD790 with mask0x1F, and calls through it with R0=state,R1=command&0xE0. It checks flag mask0x20 after the callback, so even an initially set return flag still permits one callback. Source retains the reference void(NNSG3dRS*,u32) command-entry type.

The native connected fixture runs the original table and original NODEMIX0x02030F58 followed, when necessary, by native RET0x0202FB70. RET callback slot at state+0x10 is explicitly zero. All8 upper command-bit classes and initial flags0/0x40/0x20/0x60/0xFFFFFFFF/0x80000000 yield48 original/C pairs,96 actual top returns,144 actual native command-callback returns and696 actual lower native return instructions. Total840 native returns is a sum of those disjoint categories. Tail-linked lower helper entry completions remain separate:1,132 completed native invocations total. No supplied functions are used; original table/data and existing functions gain no duplicate credit.

Every register,CPSR,full RAM including stack,MMIO shadow,raw callback/helper words and ordered writes agree. A snapshot at the actual NODEMIX entry and actual return permits the frozen754 independent weighted-matrix/nonstack/bus model to run without rewriting its inputs or inventing public registers. In this real dispatcher context the three incidental matrix-send stack words naturally contain actual entry R4=state,R5=table,R6=the preserved outer value. They remain physical storage observations,not matrix fields or extra source parameters.

Three genuinely compiled/private-linked wrong sources actually return and are independently rejected: checking the return flag before the first callback,preparing the wrong upper option word,and clearing bit0x20 instead of0x40. The option-word rejection is a caller preparation contract; NODEMIX itself does not consume incoming R1. This does not turn an unused source formal into a required callee input.

State/command/model/cache/matrix readback values are explicit synthetic setup. The fixture proves this bounded ordinary library dispatcher chain; it does not establish full rendering,game-scene entry,other command callbacks or lifecycle. Hardware registers are static ready shadows,not a coherent GPU. NODEMIX count remains1..64 with bounded arithmetic; zero/busy/dirty/malformed domains remain outside this source proof. Parent module/ROM/regression acceptance is still required. All frozen754/748/750/752 source and evidence remain unchanged.
