# Ordinary reward-state caller recovery, 2026-10-29

The measured B2JJ ROM identity remains SHA-256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`. This note addresses the application's request for ordinary reward callers. It does not certify a complete ordinary encounter, combat engine or player-reachable lifecycle.

Overlay1, ARM, `021E4EB0..021E54A0` is a 1,520-byte function with a matching ordinary C implementation at `src/overlays/ov001_20261029_reward_state.c`. Its verified caller signature is `u32(void)`, returning zero. The comparison uses the independently pinned base compiler with O2, speed optimization, ARM946E, soft float and inline disabled. The report records the complete flags, native/source/object hashes, genuine MWLD proof and immutable linked artifacts. The qualified overlay1 input SHA-256 is `39fc7aab33ce02b1910cb8fac58dd9e19936c468f3d03d1ec17dfdc8fe40ce92`.

Run `python match_ov001_20261029_reward_state.py`. The report is `evidence/matches/ov001-20261029-reward-state.json`. Standalone matching precedes coordinator registration and full-module acceptance; only an accepted cohort report supplies that later status.

The recovered function uses two sequential state chains and later common completion checks. Treating the chains as compiler-balanced switches changes the output. The table at overlay1 `02238D10` contains halfwords, not bytes. The four-byte marker view at `0222EC40` is accessed as signed bytes; assigning named gameplay meanings remains unsupported. Explicit byte-array access preserves the measured aliasing and compiler schedule without inserted instructions or encoded executable bytes.

| Qualified object | Measured fields and roles in this caller |
| --- | --- |
| overlay1 `02238CD4` | +04 u8 state; +0A u8 gate; +21/+23 s8 countdowns; +22 s8 gate; +24/+25 s8 selectors; +26 u8 halfword-table index; +30/+34 s32 state inputs |
| overlay1 `0222EC40` | +02/+03 signed-byte markers; initialized, tested together and updated by this caller |
| overlay1 `02238D10` | u16 table read for item-helper and inventory-delta arguments |
| main `0202A634` return | pointer whose +02 u16 input is masked with `0FF7`; the fixture supplies synthetic input |
| overlay1 `021F1A44` return | selected object +23 byte is cleared on one exit path; +1C word gates cleanup |

The direct qualified caller found in overlay1 is ARM `021E65A8`/336B, with a BL at `021E6630`. The matcher regenerates this static edge from measured module bytes. Indirect dispatch, the parent's incoming scene state and ordinary player reachability remain unresolved.

In state 13, overlay1 `02213630` must return zero before rewards advance. The parent calls active reward `021E49D0`, conditionally calls `022071F8` when its result is zero, then calls stock reward `021E4C34` followed by `021E4B34`. Nonzero active-reward return selects state 14; zero selects state 15. The state machine alone does not establish eligible recipients or a win/capture label for the entering state. Earlier record-byte `0x33` filtering and growth proofs retain their own evidence and limits.

State 5 passes the selected u16 table value to main `02047D40`, then to main `020630E4` with delta +1. The typed table and delta are verified in the unit fixture, including values 256 and 65,535. The actual inventory callee is replaced by an explicit provider in this particular caller test, so it supplies no new whole-inventory or valid-item-domain proof.

The unit oracle performs 704 deterministic cases and 1,408 actual native/linked returns on fresh machines. It compares R0–R12, SP/LR/PC/CPSR, whole mapped RAM, stack, instruction traces, and all CPU store addresses/sizes/values/order. An independent Python model checks post-state and complete external call order for states 0–19, 20 and 255, signed countdown boundaries, u16 table values, synthetic selectors, input masks and declared helper results. It bounds execution to 10,000 instructions and rejects any nonreturn or write outside the declared fixture regions.

All external callees in this oracle use return-only synthetic providers. They do not perform native reward, inventory, rendering, allocation or scene execution. The original dependency functions and SCR assets receive zero new source credit. The source byte match covers the complete caller; the semantic proof covers its declared transition domain. Full ordinary battle execution, real reward preconditions and the original scene's state initialization remain backlog.

The connected extension `python reward_connected_20261029.py` now executes the original 336-byte dispatcher through its real callsite at `021E6630`, with context byte `02238CEA` (+0x16) equal to 1. It reaches exactly one real reward-parent invocation and returns zero in all 704 cases per implementation (1,408 actual returns), with the same independent state/call-order model, full RAM/stack, register and trace comparisons. The rebuilt variant replaces only the parent with its immutable source-linked bytes; the dispatcher is already accepted source elsewhere and adds zero new credit. All external parent providers and scene-initialization limits remain unchanged. Results are in `evidence/application/reward-connected-20261029.json`.
