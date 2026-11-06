# Cohort 74 heap, range and serialization source — 2026-10-31

The accepted build has 8,848 matched functions and 654,785 source-linked initialized bytes: 26.0596839% of 2,512,636 inventoried initialized module bytes. Sixteen ordinary C functions add 3,268 bytes, preserving every earlier selected source/object and all 27 primary preferences. There are 634,050 function bytes including pools, 20,711 data bytes and 24 padding bytes; unresolved initialized coverage is 1,857,851 bytes. Neither an executable-only denominator nor overall game completion is proved.

| Packet | Functions | Initialized bytes |
|---|---:|---:|
| Decimal record caller | 1 | 168 |
| Range-key helpers | 2 | 272 |
| ARM7 sound-bank parser | 1 | 384 |
| ARM7 heap constructors/setter | 3 | 380 |
| ARM7 allocation/list/release | 3 | 548 |
| ARM7 heap checker | 1 | 416 |
| Gated record byte exchange | 1 | 28 |
| Wide-number caller | 1 | 300 |
| ov006 layout caller | 1 | 240 |
| ov001 gate caller | 1 | 312 |
| ov006 dialog caller | 1 | 220 |

All 20 module comparisons pass, along with two exact checksum matches, 36 vectors/144 isolated actual checksum returns, 5,117 getter comparisons, freshness rejection checks and authored-source policy. The scaffold-assisted ROM is exactly 175,959,612 bytes with SHA-256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`. Baseline/original input hashes remain unchanged. Concurrent application edits retain a failed strict whole-workspace isolation result. Source-only ROM, complete Windows game, Android execution and full clean replay of this exact cohort remain unproved.

The [decimal caller](2026-10-31-decimal-caller-and-abi-drafting.md) passes 1,952 top-level original/source returns, including 96 returns with the actual native converter and no supplied function results. The converter's output is an observed continuation fixture, not an independent arithmetic oracle. The [range group](2026-10-31-range-key-source-group.md) passes 1,874 top-level returns and 116 nested original lookup returns with zero providers; all 264 instruction bytes are observed, plus eight literal bytes. A too-large negative-control implementation was refused before injection. The initial header-dependency registration schema failure was repaired after restoring only our own partial registry update; no accepted source was changed.

The ARM7 sound-bank parser is unrelated to save-bank arbitration. It checks all 256 type bytes, partial-output failures, inclusive bounds and split positions across 1,892 top returns, with mutex leaf returns separately counted. Constructors/setter pass 1,536 top returns and 39 controls; allocation/list/release pass 1,004 top returns and 39 controls; the checker passes 512 top returns and 37 controls. All use original native prerequisites rather than function-result providers. The checker tests the OS global arena, not ownership within the initially constructed heap. Out-of-heap but in-global-arena returns do not become an ownership/import rule. Signed-sum overflow and unsupported impossible branches remain excluded.

The byte exchange preserves the full-width absent sentinel: gate word at +0x30 equal to zero returns FFFFFFFF without reading/writing record byte +0x1; otherwise it returns that old unsigned byte and writes the new low byte. Old byte FF returns 000000FF, distinct from absence. Its 12,288 actual returns have zero providers. The 300-byte caller passes 6,400 actual returns, executing the original 8BE0 fill and 211C0 variadic adapter. Only lower formatting is provided; no locale, truncation or scene guarantee is inferred.

The overlay layout packet passes 128 caller returns and 1,280 original helper returns, with 3,040 explicit UI providers. Its helper produces a raw integer word, not a pointer declaration chosen to force equality. Gate and dialog packets respectively pass 1,152 and 128 top returns, with 1,244 and 1,034 explicit lower providers and no actual dependency credit. Their shared producer is replayed through `reproduce_overlay_packet95_20261031.py`, which regenerates and seals both reports together so replaying one cannot leave its sibling unsealed.

A separate [connected save proof](2026-10-31-connected-save-serialization.md) rebuilds 21 already accepted C functions together and adds zero coverage. Its 82 original/source pairs give 164 actual host returns plus eight negative-control returns. Date/time/allocation/asynchronous-request boundaries remain four explicit providers. Full payload serialization includes primary flags at offset 3994, whereas the shorter copy ending at 393C omits them. Measured validator precedence and raw callback thresholds remain conditional buffer-local behavior; chronology, device completion and save-bank selection are unproved. All 40,560 semantically unknown save bytes remain unknown.

Acceptance is `evidence/verification/cohort-2026-10-29-74.json`; the 16-command build is `cohort74-validation-driver.json`. Replay with `python run_cohort_20261031_74.py` and `python finalize_cohort_20261031_74.py` before later registry adoption. The independent immutable checkout U continues on its earlier committed snapshot and does not certify this cohort.
