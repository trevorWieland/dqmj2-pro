# Native ability flags and summary text source, 2026-10-31

This private handoff contains two ordinary C candidates whose complete native spans match through fresh pinned compilation, ELF relocation checks and genuine MWLD linking. It changes no registry, accepted source, module builder or application file. Integrator acceptance remains pending; this packet assigns zero accepted source credit.

The authoritative ROM has 175,959,612 bytes and SHA-256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`. Both entries are ARM9 ARM routines. Overlay identity is mandatory despite the common load base `0x021D7240`.

| Module | Entry | Native bytes | C source SHA-256 | Header SHA-256 |
| --- | --- | ---: | --- | --- |
| ov001 | 0220FA6C | 788 | 8dfc73fd4fabc3aa8626079d64f2e715dd1c4b8f3431eb91f73b73ae2288ca35 | 250e65fd3b8edf112792b0769725e470605088f7e57fb2df85f97632418b6902 |
| ov006 | 021DCB20 | 508 | a040fede8fc7f4611a97f05d3dc31caca93d3716bc8063a3c31387f57e4c5397 | b4c569e9d0e51d8392f05ebd993e2a787f4d92a369927825c118b58863ef91ed |

The module input hashes are ov001 `39fc7aab33ce02b1910cb8fac58dd9e19936c468f3d03d1ec17dfdc8fe40ce92` and ov006 `fb9cb28ea400207bda442e3265da73af994866cf3a6c352b46a11db59835d341`. Main input is `ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f`. Reports preserve compiler profiles, object hashes, relocations, qualified addresses, linker commands and frozen link snapshots. No assembly, padding, opcode changes or invented register arguments are used.

## ov001 flag caller

The source performs twelve ordered raw-ID lookups through main `0207B674`, passing the record word at actor+0x1E8 plus0x46 as R1. A signed positive lookup result permits a call to ov001 `02210AD0`, with the actor in R0 and the measured two constant argument words. A nonzero gate result ORs one measured mask into actor+0x33C and sets the physical return accumulator to1. All other actor bits survive. Already-set bits still produce return1 when a gate succeeds. A caller with no successful gate returns0, regardless of preexisting flags. Raw IDs, constants and masks are listed in the report; they do not establish human ability names or probability semantics.

Using the same return-flag OR expression in the first branch as in the other eleven branches closes the previous single-byte instruction-selection difference. The independent model derives expected provider order, signed comparison behavior, flag updates and write order from a separate rule table. It validates all RAM, preserved registers and actual return. The original and rebuilt executions additionally compare all general registers, condition flags, full RAM, private stack, PC trace and write trace.

There are138 deterministic synthetic recipes and276 actual top returns, with4208 explicitly provided lower calls and no native lower-callee execution credit. Cases isolate every ID, cover signed lookup extremes, zero/nonzero full gate words, mixed eligibility, unrelated initial flag bits and already-set flags. Maximum native caller instructions are197. A separately compiled and genuinely linked wrong-mask C control is rejected by the independent complete-memory/write-order model. Neither provider establishes actual RNG behavior, metadata validity, lifecycle or whole-battle reachability. The two lower-call interfaces are observed call words in this scope, without a universal pointee-extent or hidden-input claim.

## ov006 summary caller

The source owns the actual `u16 text[32]` output buffer. The previous scalar placeholder omitted the required64-byte capacity and generated a shorter frame. The array matches all508 native bytes without artificial stack padding. Native output bounds are the72-byte local area below the saved R4/LR pair, excluding the8-byte outgoing stack-argument area. The fixture checks every format destination and consumption at lengths0,1 and31 plus NUL.

Actual main getters `020679F0`, `02067748`, `0206442C` and raw-ID transform `020643FC` execute in the measured image and return normally. The first getter reads the root at `021C3708` and its pointer at+0x2C. Identifier getter executes twice. IDs0,1,46,47,239,240 and65535 exercise the measured transform boundaries. Synthetic numeric source fields include modest signed positive/negative values; field0xC is0..7, and arithmetic avoids signed-overflow extrapolation. Five numeric outputs, their ordered labels, name formatting, raw-ID display and transformed-ID display are checked independently. UI and formatting routines remain explicit providers; supplied words do not establish actual text encoding, rendering or loaded-resource reachability.

There are56 deterministic recipes,112 actual top returns,560 actual native dependency returns and2912 provided services. Maximum native instructions are146. A separately compiled/genuinely linked scalar-output C control is rejected at the buffer-bound gate. Final physical R0 remains the final display provider word, with no semantic return interpretation.

## Portable replay and identities

Run `python match_overlay_packet28_20261031.py` from this repository. Alternatively run `python C:\Users\trevo\Documents\RecProgramming\DQM\j2p-recovery-lanes\overlays\match_overlay_packet28_20261031.py` from an unrelated directory. The script resolves every input, output and tool independently of the working directory. Python3.13.5 and Unicorn2.1.4 are required. Its two independent reports are `evidence/matches/ov001-20261031-ability28.json` and `evidence/matches/ov006-20261031-summary28.json`.

Normal and alternate-directory replays compare the complete report content excluding only volatile `createdUtc`. Their content digests are respectively `f4c13b3cdd578c11bf83ef5e8f3749d5e9351b01cf195d3c6c8cfd1067a4e001` and `c963baaa9092329854e439ee3090828f8888f73497ff8c630f37147c820395b9`. A manifest pins the handoff-file hashes for transfer integrity; those full-report hashes are snapshots, not stable replay identities. Full cases and traces are checked during execution and serialized into deterministic hashed gzip artifacts under `work/ol28-proof`, excluded from the source-only handoff and regenerated locally.

Whole-module/ROM acceptance, original asset and executable replacement accounting, clean source rebuilds and all prior regressions remain integrator gates. No draft, provider, unchanged original native dependency or successful repack gains source credit here.
