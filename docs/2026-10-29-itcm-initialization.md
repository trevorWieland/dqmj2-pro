# ITCM initializer, 2026-10-29

The complete 520-byte ARM9 ITCM function at `0x01FFA988` now matches ordinary C. Fresh compilation and actual MW linking reproduce all 123 instructions and the 28-byte literal pool. No assembly, instruction patch, original executable object, or embedded executable byte array contributes to this caller body.

The recovered operations initialize several state fields, pass a four-byte pair of coordinates through native calls, execute a four-iteration loop plus additional calls, handle an optional actor field, and reset several global fields. Broader gameplay meanings and original declarations remain unproven.

## Reproduction

Run `python verify_itcm_20261029_initialization.py`, or invoke that script by absolute path from another working directory. Its frozen inputs are `src/itcm/20261029_initialization/native_itcm_01ffa988.c` and the adjacent header. It writes `evidence/matches/itcm-20261029-initialization.json` only after every gate passes.

The source and header hashes are pinned independently. Compiler settings are demonstrated for this unit: the pinned MW 2.0 base compiler, ARM946E, `-O2`, and `-inline off`, without a speed override. Previous mutable compiler outputs are removed. Every original code/data relocation is retained and resolved by the actual pinned linker. Function bindings validate build/module/address/mode identity separately for main, ITCM, and overlay `ov000`; global bindings additionally require configured data/BSS symbols.

The real caller link supplies no executable callee bodies. Canonical mode anchors contain zero initialized callee bytes and contribute zero callee source credit. This isolated caller match remains distinct from an accepted whole-module source build.

## Closing the final mismatch

The scalar draft reached 514/520, but interleaved a local halfword store between the two global halfword loads. An actual four-byte structure copy reached 516/520 while copying the two fields in the opposite order.

The final C reads the two unsigned halfwords into ordinary scalar temporaries, then stores them into the four-byte local point. Volatile qualifiers on the source record and local point express the measured load/load/store/store ordering. This is a reconstruction choice that reproduces observed native behavior; it does not establish that the historical source used those qualifiers. The field offsets, halfword widths, point size, and generated instructions remain unchanged.

Address-compatible extern object alignment hypotheses used the suffix `__attribute__((aligned(N)))`, retaining true field offsets and types. Those hypotheses did not close A988, C890, or F068. Prefix declaration variants that changed wider code generation were rejected independently and are not accepted object-layout evidence. All experiments remain under `work/lowlevel-recovery/20261029-itcm/`.

## Independent bounded checks

Seventy-two paired fixtures produce 144 actual returning executions in fresh native/source Unicorn machines. Both ARM and Thumb returns, inactive/active actor fields, coordinate extremes/random coordinates, signed-byte boundaries, and getter-result truncation are covered. All 123 caller instructions execute across the fixtures.

The independent model checks complete ITCM/global/object pages, typed and ordered global stores, both coordinate halfword reads and their order, every native call and register/stack argument word, the exact four-byte point contents, preserved R4–R11/SP, and return modes. The formerly omitted six-word, nine-word, and seven-word interfaces are checked directly against registers and the outgoing stack. Complete register state, NZCV, native stack writes, and page hashes additionally agree between native and source runs. LR is caller-clobbered in this nonleaf function's return sequence; actual return to the sentinel is required.

All external implementations are deterministic return/ABI-clobber contracts. They provide context for the caller without claiming recovered callee behavior. No game hardware, asynchronous global updates, invalid actor pointers, or complete overlay lifecycle behavior is established by these isolated fixtures.

Shared ledger registration and accepted module builds remain the integrator's responsibility. Earlier partial drafts receive no source credit.
