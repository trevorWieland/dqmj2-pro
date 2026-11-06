# Native reward byte copy, 2026-10-29

Ordinary C reproduces overlay1 ARM021E6720/36 bytes, including its destination literal. A genuine pinned MWLD link matches the complete native span. The integrator owns final whole-module acceptance.

Replay `python match_ov001_reward_copy_20261029.py`; the report is `evidence/matches/ov001-20261029-reward-copy01.json`. Compiler2.0 base, O2, speed optimization and disabled inlining match this unit. Python3.13.5 and Unicorn2.1.4 are required. Repository-local inputs and outputs resolve independently of working directory.

The function takes an input byte pointer, copies three bytes forward into overlay1 data02238D18, and returns the original input pointer through R0. The destination's larger game meaning is unresolved. The remaining reward-pool routine ARM021E3BE4 reads these bytes in its three-enemy loop; that caller is still unmatched.

Ninety-six vectors produce192 actual native/linked returns. They include separate aligned/unaligned inputs, exact source/destination aliasing and source offsets minus4 through plus4 around the destination. An independent sequential byte model reproduces propagation through overlapping ranges. Every case uses fresh randomized machine state. All mapped RAM, the complete stack, preserved registers, return pointer, ordered writes and instruction traces agree. There are no callee stubs.

Invalid/unmapped inputs and concurrent mutation remain unsupported. The implementation contains ordinary byte loads/stores and loop logic; original executable bytes are not encoded in source. Earlier accepted source and fixtures remain unchanged.
