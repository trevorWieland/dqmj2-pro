# Battle/reward state family C, 2026-10-29

Five additional overlay1 ARM routines now have frozen ordinary C, exact whole-function compiler/ELF comparisons, genuine pinned MW links and 2,624 independent vectors/5,248 actual-return native-versus-linked caller/provider executions. They total 2,712 native bytes. Whole-module and ROM acceptance remain the integrator's separate gates.

The measured ROM SHA256 is `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`; overlay1 initialized-image SHA256 is `39fc7aab33ce02b1910cb8fac58dd9e19936c468f3d03d1ec17dfdc8fe40ce92`. CPU is ARM9, every recovered entry is ARM, and all context accesses are module-qualified uses of `02238CD4`. Main fixture image SHA256 is `ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f`.

| Entry | Bytes | Principal state byte | Profile | Executions |
|---|---:|---:|---|---:|
| 021E54A0 | 408 | +20 | MW2.0 base, O2 + speed | 1,024 |
| 021E5638 | 760 | +18 | same | 1,408 |
| 021E5E04 | 388 | +10 | MW2.0 base, O2 | 768 |
| 021E5F88 | 604 | +0E | MW2.0 base, O2 + speed | 1,024 |
| 021E634C | 552 | +09 | MW2.0 base, O2 | 1,024 |

Offsets are hexadecimal. All profiles retain inline off and the established pinned ARM946 compiler settings; no profile is generalized beyond its measured source unit. Frozen sources are the five `src/overlays/ov001_20261029_reward_<address>_<hash>.c` files. Their exact paths/hashes, object hashes, complete byte comparisons, qualified bindings, ELF relocations and actual MW linker artifacts are in `evidence/matches/ov001-20261029-reward-worker01.json`.

The C expresses the native sequential if/else state chains. Subsequent independent if blocks can process a newly assigned state in the same call; treating the whole routine as one switch changes that behavior or code generation. Global byte preincrements preserve the measured raw store, wrap and promoted comparison forms. The 760/604-byte routines also require the existing accepted two-argument ABI of overlay1 `021E3564`, supplying raw operands20/21 and1. Earlier m2c output omitted arguments still live in registers. The accepted callee's source/hash is recorded as a zero-credit ABI dependency.

Recovered effects remain raw native observations. The routines update byte state/selectors, signed byte timers/handles, and, in the 552-byte routine, a signed halfword timer at+28. The latter also clears an entity byte at+23 after an external entity provider and tests its word at+1C. These field offsets, widths, transitions and call operands are measured; gameplay names, victory/loss meanings and save persistence are not certified.

The independent model covers every observed state value plus unknown255, argument words0/1/8/9/10/11/FFFFFFFF/80000000, byte counters including254/255 wrap, signed timer boundaries, signed handles127/128/255, masked/unmasked input bits and busy/provider results0/1/2/FFFFFFFF. It checks complete context/entity effects, preserved RAM, call order, known argument words, short-circuit calls and same-call transitions. Each machine starts fresh with deterministic randomized registers, CPSR, other context bytes and stack bytes. Every execution must actually return within10,000 instructions, preserve SP and the callee-saved registers, and return zero. Native/linked execution also compares every R0-R12 value, CPSR, complete RAM/stack hashes and PC/write traces.

These are explicitly caller/provider tests. Every external function uses a qualified-mode return-only provider that changes R0, restores the return instruction mode and performs no memory writes. Native external scene, rendering, inventory, reward and input/entity bodies are not executed. Other native callee register/memory/hardware effects and live scene reachability remain unsupported. Synthetic fixture seeds are not measured current or future game RNG state. No whole-scene or additional callee source credit is taken.

Canonical interval checks found no accepted overlap for the five assigned spans; the audit is retained at `work/ov001-reward-worker/20261029/reservation-audit.json`. Root's accepted/owned parent, selector, exit and dispatch routines remain unchanged. No shared registry, ledger, builder, application adapter or existing SDK source/fixture was edited.

Replay:

```text
python match_ov001_reward_worker_20261029.py
```

Use pinned Python3.13.5, Unicorn2.1.4 and repository-local MW tools/license. Scripts derive paths from the repository location. Source, matcher, fixture and independent model are comment-free and each remains below500 physical lines. Earlier switch, narrow-temporary and incomplete-arity hypotheses remain under `nonmatching/ov001/20261029-reward-worker01/` and receive zero credit.
