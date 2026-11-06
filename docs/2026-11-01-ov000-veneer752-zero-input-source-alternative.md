# ov000 zero-input veneer source alternative, 2026-11-01

ROM SHA-256: 674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6.
ARM9 ov000 SHA-256: 783cb72f0d6ee2fdb632aba3e0ae41a9eee0c7e41933192b1680152e50aa61f6.
Identity: ARM9, empty program namespace, ov000, ARM 0x022198E0, 12 bytes.

The new source defines u32(void) and calls 0x022198EC with an explicit u32(void) declaration. The pinned compiler and genuine MWLD reproduce all existing 12 bytes: two ARM instructions and one literal word. This is an alternative to an already selected four-word transplant. It adds zero functions and zero initialized source bytes. The old transplant, packet 750, registry and preferences remain unchanged. The integrator owns coordinated migration and selected-caller interface review.

Reproduce from the repository or any other working directory with Python 3.13.5:

    python C:/Users/trevo/Documents/RecProgramming/DQM/j2p-recovery-lanes/overlays/match_ov000_veneer752_20261101.py

The run compiles and genuinely links fresh source, then executes original and linked candidate entry code under Unicorn 2.1.4 CPU946 with isolated machines. It retains the original 80-byte 0x022198EC target and original main 0x0205F98C leaf. There are no providers. The target terminal return is the veneer top return and is not counted again as a dependency.

Each of 160 resource/global/object states is repeated with all four cyclic permutations of R0-R3 over 0, 1, 0x80000000 and 0xFFFFFFFF. All 640 pairs compare every core register, CPSR, full RAM including stack, raw leaf call words and ordered writes. They produce 1,280 actual top returns and 512 separately watched actual native leaf returns. Within each global/object state, the raw R0 return and complete nonstack effects are identical across poison rotations. Unused caller-saved words and saved stack values can still carry entry poison; independence is not asserted for those incidental values.

The independent model distinguishes resource sentinel 127, null object pointer and a nonnull 128-byte object. Active cases set or clear mask 2 at object offset 0x7C according to the unsigned byte at 0x02245E55. Raw R0 is 127, zero or the object pointer respectively. The existing main 0x0205F98C u32(s32,s32) facade is retained with index zero. Two genuinely compiled/private-linked wrong source controls actually return and are rejected: incrementing the raw result, and skipping the target. Full deterministic traces are separately hashed gzip; compact case hashes and counts stay in the report.

This establishes zero required physical input words in the measured closure, not the original unused formal count or game meaning. Globals and object bytes are explicit synthetic inputs. Invalid pointers, aliasing, allocation lifecycle, actual scene reachability, other callers, application behavior and host/device execution remain unqualified. Integrator module/ROM/regression validation is still required before preference adoption.
