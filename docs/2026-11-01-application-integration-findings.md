# Application integration findings — 2026-11-01

All addresses below refer to modified B2JJ ROM SHA-256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`. Original game inputs and the application are not edited. Matching bytes, synthetic native execution and actual scene reachability are separate evidence classes.

## Full-word forwarding at main ARM 020380E4

The complete wrapper is 16 bytes at 020380E4. It loads the pointer held by its first argument and tail-forwards incoming R1 to the complete 40-byte target at 020385A0. The target first accepts a null pointer, otherwise compares the entire R1 word against the unsigned byte at object+2E. When unequal it passes unsigned object byte+3C to 02009128, then stores the low eight bits of the original R1 at object+2E. A word equal only in its low byte still takes this unequal path.

The reconstructed wrapper uses an explicit pointer-holder argument and unsigned word argument, with a void C result. Native R0 is recorded without assigning it a semantic C return value. `python match_main_resource_word_forwarding_20261101.py` genuinely recompiles and links the wrapper, checks 4,096 original/C returns, and runs 4,096 returning zero-word/byte-truncation controls with 1,401 rejections. The actual original target body executes; the lower 02009128 call remains an explicit supplied service. This replaces an incomplete one-input prototype through a zero-credit source-preference migration after acceptance. No original typedef, field meaning or service behavior is inferred.

See `evidence/matches/main-resource-word-forwarding-20261101.json` and the save lane's `evidence/matches/mechanics-save-20261101-lane-status-inputs.json` for the measured caller domains. The status packet contributes four new main ARM callers: 0205F27C/92, 0205F404/88, 0205F45C/76 and 0205F848/88. Its 7,928 top returns and 16,992 physical helper returns retain software division and shared-label execution. Logical tail entries do not receive duplicate physical-return credit. Supplied 02009128/0203A4FC boundaries and unsupported paths remain explicit.

## Larger overlay1 action draft

`python qualify_ov001_action436_20261101.py` tests the complete 1,232-byte overlay1 ARM caller at 021EA56C as ordinary C. All 198 original/C pairs pass, with 396 actual top returns, 5,316 actual native-dependency returns and 5,340 supplied service calls. The 420 RNG returns are included in the dependency total. Twenty-four compiled wrong-state/wrong-debit controls return and are rejected. The actual caller's 1,220 instruction bytes are observed; the remaining native bytes are literals.

Native RNG/division, actor resolution and validity, class lookup, resource update and clear helpers execute. Initialization, query, policy and notification prerequisites still include supplied boundaries. Linked C agrees at 1,213 of 1,232 byte offsets and remains outside accepted exact-byte coverage. This supports a bounded action-state hypothesis, not full ordinary battle execution, player-controllable future RNG or ordinary-scene reachability. The manifest `provenance/handoffs/ov001-action436-functional-20261101.json` preserves the worker evidence; the root replay is recorded in `logs/integration/overlay-action436-replay-20261101.txt`.

## Allocation and portability

Main ARM 0202A37C/172 checks the low index byte for its range test, then indexes with the entire word. Its bounded synthetic input domain must not be generalized to arbitrary words sharing a valid low byte. Main ARM 0202B334/48 rounds lengths modulo 32 bits and dispatches according to alignment direction. Lower allocator outcomes are explicit contracts in their matching packet.

The two fresh C sources also build for Windows x64 and Android AArch64 API 33. `python verify_windows_allocation_ports_20261031.py` checks 1,764 actual Windows calls and full declared allocator state with data addresses above 4 GiB. Android device executions are zero. Three larger allocator C drafts have separate connected behavior evidence, with original remaining helpers executing and no supplied outcomes; their compiled bytes still differ. See `docs/2026-11-01-cohort98-allocation-and-draft-validation.md`.

## Work still needed for the application

The reward-entry investigation is tracing overlay1 021E49D0, 021E485C, 021E4C34 and their ordinary caller/selector setup. Current leads are not adopted predicates. Encounter availability and repeatability, saved progression semantics, ordinary battle lifecycle, recruitment scene initialization and persistence of the RNG state still require source and caller evidence. These findings do not reduce the semantically unknown save-byte partition or convert conditional native checks into unconditional import restrictions.
