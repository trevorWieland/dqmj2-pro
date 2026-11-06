# ARM7 player/track flag initializer source — 2026-10-30

Host ARM7 WRAM ARM 037FFEF0 rebuilds from complete ordinary C and real pinned Metrowerks linking to 100 initialized bytes: 92 instruction bytes and 8 compiler-generated literal bytes. It clears only bit 0 in 16 successive 36-byte player records at 03808420, stores each player's index 0..15 into byte+1, then clears only bit 0 in 32 successive 64-byte track records at 03808660. Other flags and record bytes remain unchanged. The API is void; incidental R0 is compared only as CPU state. There are no callee calls or replacements, and no data/BSS/anchor/module/ROM credit.

The independent corpus uses 257 fresh machines with all 256 initial flag values per record, deterministic varied neighboring data and one two-call persistent case. It produces 516 actual original/recompiled entry returns and 64 ordered byte stores per invocation. Original and source agree on all general registers, CPSR, entire mapped RAM/BSS/stack and ordered writes. A separate byte-level model checks every selected flag/ID store and preservation of all other bytes. Every own instruction address is visited. One-instruction exhaustion is separately retained with zero return/error-result credit. These are bounded SDK-record effects; enclosing scene reachability, physical audio and full game/save initialization are not asserted.

The first ordinary C draft reused one loop index and emitted the second loop counter in LR. A separate ordinary int track_index ends the first variable's lifetime and reproduces native R2 allocation, closing all code differences. No assembly, volatile, register forcing, encoded instructions or changed relocation addends are used. The source is standalone and comment-free under src/arm7/20261030_seq_init. Reference-only support is the byte/Git-verified pokediamond SND_seq.c at b623abef1b4dfe204ca50aab42447ac00c134290, SND_SeqInit. No same SDK version or unique original compiler settings are presumed.

The matcher measures full source linkage, configured 92-byte ARM range, two 4-byte pool words, outside direct-flow/interior-word audits, source/object/compiler/runtime hashes and qualified original BSS bindings. It writes the canonical report itself. The standalone validator freshly recompiles and reruns every vector, checks current products after caching and passes 31 rejection controls. These include wrong cleared flag, omitted player-ID store, shortened player/track loops and actual wrong-C constant-ID compilation/link rejection. It restores the positive compiler products afterward. All prior accepted/frozen files remain unchanged and the coordinator owns module/registry acceptance.

Reproduce with the pinned absolute interpreter from any directory:

```
C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\match_arm7_seq_init_20261030.py
C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\validate_arm7_seq_init_20261030.py
```

Canonical evidence is evidence/matches/arm7-seq-init-20261030.json; controls are evidence/verification/arm7-seq-init-controls-20261030.json. This clean contiguous 100-byte routine is separate from the adjacent discontiguous 037FFF54 boundary proposal. Neither execution proof approves that proposal or adds its 64 code bytes to source credit. The initializer is queued for 59 or later; complete module acceptance remains pending.
