# Reward entry selector and follow-on state, 2026-10-29

Accepted cohort 38 reconstructs two more complete overlay1 ARM functions: `021E3764..021E3B34`/976B and `021E5AC8..021E5CF8`/560B. Both have caller signature `u32(void)`; the selector returns one and the follow-on returns zero. The measured B2JJ ROM and qualified overlay1 hashes are unchanged. Canonical evidence is `evidence/matches/ov001-20261029-related-states.json`, reproduced by `python match_ov001_20261029_related_states.py`.

The base compiler's per-unit O2/speed profile, ARM946E/soft-float settings and genuine MWLD links match every initialized byte and declared relocation. Complete source, object, native span, ELF, LCF and immutable linked-artifact hashes are recorded. Source files are `src/overlays/ov001_20261029_entry_selector.c` and `ov001_20261029_exit_state.c`. Sequential if/else chains and byte lvalue increments reproduce the original control flow; no assembly or instruction-byte replacement is present.

The selector reads overlay1 context `02238CD4+02` as u8 and writes +16 as a byte. Its six preparatory helper returns are forwarded as raw words to the original five-word `021E36C4` call, including its stack argument. Those words do not acquire inferred species, participant or formation meanings from this fixture.

| Raw context +02 at the selection point | Resulting context +16 |
| --- | --- |
| 0 | 13 if main `020444EC` returns nonzero; otherwise main `020443EC` values 5/6/7 select 13/14/16, and other values select 1 |
| 1, 2 | 2, 3 respectively |
| 3, 4 | 4 |
| 6, 7 | 5, 6 respectively |
| 8, 9, 5 | 7, 8, 9 respectively |
| 10, 11, 12 | unchanged numerical value copied to +16 |
| Other measured byte values | +16 remains unchanged |

The already accepted dispatcher `021E65A8` calls this selector for +16 equal to zero and repeats dispatch when the selector returns one. Its +16 equal to one branch calls the newly reconstructed reward parent `021E4EB0`. This supplies a measured static transition chain under the declared synthetic helper contracts. The original preparatory helper bodies may affect context; an initial +02 value alone is not a complete ordinary-scene prerequisite.

The follow-on function reads/writes context +13 as u8 state and +12 as a wrapping u8 counter, writes +16 on completion, and passes the s32 word at +2C and its negation to dependency calls. The oracle bounds the amount to 0/1/300/65,535 and excludes signed-negation overflow. It verifies counter boundaries 0/1/2/29/30/31/254/255, same-invocation transitions, completion short circuits and declared argument order. It does not assign win/loss, price or currency meanings to those raw states or fields.

The independent Python transition/call-argument models pass 512 selector and 320 follow-on cases: 1,664 actual native/linked returns on fresh machines. Comparisons cover R0-R12, SP/LR/PC/CPSR, whole mapped RAM/stack, CPU store order/addresses/sizes/values, instruction traces, and the selector's fifth stack argument. Each run has a 10,000-instruction/2,000,000-microsecond bound and must reach its return sentinel.

All external calls use explicit synthetic return-only providers here. Actual scene preparation, reward recipients, inventory/currency mutation, rendering, and player reachability remain unsupported by this caller test. Native state control and exact source bytes have separate evidence from gameplay interpretation. The later complete module/ROM checks pass in cohort 38 with all earlier matches preserved; original executable gaps and interpreted scripts remain scaffolding.
