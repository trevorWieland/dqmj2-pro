# Weak DATA-OR-STUB rows: what the 61 actually are

Generated from `work/inverse-weak.json` (the DATA-OR-STUB bucket of the weak-inverse
classification, PR #156). No ledger edits; `docs/data/index.json` was **not** extended (see below).

## Counts

| bucket | rows | bytes | what it is |
| --- | --- | --- | --- |
| GENUINE DATA | 0 | 0 | no row has a table/blob whose layout is constrained by a matched reader |
| STUB OR PLACEHOLDER | 57 | 15,564 | the `sourceUnit` is an include-shim whose top file only declares/includes; the real function bodies live in the included `.inc` parts |
| STILL AMBIGUOUS | 4 | 1,192 | the include parts contain an initialised array, but nothing in the box ties it to this row's address or a consumer |
| **total** | **61** | **16,756** | |

The 61 rows are **not data tables**: 53 are `arm7-main`, 6 are `arm7-wram`, 2 are `main`
code ranges (function-mode rows). Their `sourceUnit` files are 50-262-byte shims such as:

```
extern unsigned int native_host_arm7_data_0380fff4;
#include "ordinary_part1.inc"
#include "ordinary_part2.inc"
#include "ordinary_part3.inc"
```

Resolving the includes gives 27 distinct units; 60 of 61 rows have at least one function
body in an included part, and 4 rows' parts also contain an initialised array. No included
text contains the row address or the ledger symbol, so none of these rows is attributable
from its own unit - which is exactly why the earlier pass called them weak.

## Why the dictionary was not extended

`docs/data/index.json` only admits entries whose layout comes from a matched reader, with a
citing source file and function. None of the 61 qualifies: the 4 array-bearing rows have no
consumer reference to the array inside the box, and the rest are code (function bodies), not
data. Adding them would be labelling unverified bytes as a table. The honest state is
"unexplored", and they are listed below so a modder can pick them up later.

## Unattributed rows (all 61)

| address | module | bytes | sourceUnit | kind |
| --- | --- | --- | --- | --- |
| 0x27f284c | arm7-main | 1612 | src/arm7/20261102_wl_beacon_probe_key3016/ordinary_wireless.c | include-shim |
| 0x27f31fc | arm7-main | 976 | src/arm7/20261102_wl_beacon_probe_key3016/ordinary_wireless.c | include-shim |
| 0x27f3c1c | arm7-main | 804 | src/arm7/20261101_wl_element804/ordinary_wireless.c | include-shim |
| 0x37faec0 | arm7-wram | 800 | src/arm7/20261102_wl_transmit_family1600/TxCtrl-base/ordinary_wireless.c | include-shim |
| 0x27f2180 | arm7-main | 720 | src/arm7/20261102_wl_receive_data_task720/ordinary_wireless.c | include-shim |
| 0x37f8a88 | arm7-wram | 720 | src/arm7/20261102_wl_tasks_command1224/CmdDispatch/ordinary_wireless.c | include-shim |
| 0x2015c70 | main | 656 | src/runtime/parallel_wave20261106/mb-local-context-next/register/register.c | include-shim |
| 0x27ed864 | arm7-main | 624 | src/arm7/20261102_wl_measure_task624/ordinary_wireless.c | include-shim |
| 0x27eff00 | arm7-main | 544 | src/arm7/20261101_wl_tx544/native_host_arm7_main_027eff00.c | include-shim |
| 0x27ed220 | arm7-main | 496 | src/arm7/20261102_wl_mlme_tasks_timeouts860/ordinary_wireless.c | include-shim |
| 0x27f2f78 | arm7-main | 464 | src/arm7/20261102_wl_receive_helpers1092/receive/ordinary_wireless.c | include-shim |
| 0x27f25cc | arm7-main | 428 | src/arm7/20261102_wl_beacon_probe_key3016/ordinary_wireless.c | include-shim |
| 0x27f0308 | arm7-main | 380 | src/arm7/20261102_wl_interrupt_transmit1236/TxCtrl/ordinary_wireless.c | include-shim |
| 0x27f2450 | arm7-main | 380 | src/arm7/20261101_wl_rxmp380_unsigned_aid/ordinary_wireless.c | include-shim |
| 0x27f0120 | arm7-main | 360 | src/arm7/20261101_wl_tx544/native_host_arm7_main_027eff00.c | include-shim |
| 0x27f19fc | arm7-main | 352 | src/arm7/20261101_wl_frame_builders1304/ordinary_wireless.c | include-shim |
| 0x27eb9b4 | arm7-main | 320 | src/arm7/20261102_wl_cam_registration716/ordinary_wireless.c | include-shim |
| 0x27edc6c | arm7-main | 248 | src/arm7/20261101_wl_mlme_indications484/ordinary_wireless.c | include-shim |
| 0x27f0d6c | arm7-main | 248 | src/arm7/20261102_wl_interrupt_transmit1236/TxCtrl/ordinary_wireless.c | include-shim |
| 0x27edd64 | arm7-main | 236 | src/arm7/20261101_wl_mlme_indications484/ordinary_wireless.c | include-shim |
| 0x27ee0e4 | arm7-main | 236 | src/arm7/20261102_wl_control_setters_key484/Parameters/ordinary_wireless.c | include-shim |
| 0x27f0f14 | arm7-main | 232 | src/arm7/20261102_wl_transmit_family1600/TxCtrl-sp1p5/ordinary_wireless.c | include-shim |
| 0x27ec5a4 | arm7-main | 228 | src/arm7/20261102_wl_cam_registration716/ordinary_wireless.c | include-shim |
| 0x27f2e98 | arm7-main | 224 | src/arm7/20261102_wl_receive_helpers1092/receive/ordinary_wireless.c | include-shim |
| 0x27f1e08 | arm7-main | 192 | src/arm7/20261101_wl_frame_builders1304/ordinary_wireless.c | include-shim |
| 0x37f8598 | arm7-wram | 184 | src/arm7/20261102_wl_tasks_command1224/TaskOps/ordinary_wireless.c | include-shim |
| 0x27f17d4 | arm7-main | 180 | src/arm7/20261101_wl_frame_builders1304/ordinary_wireless.c | include-shim |
| 0x27ef548 | arm7-main | 176 | src/arm7/20261102_wl_control_setters_key484/Device/ordinary_wireless.c | include-shim |
| 0x27f3b6c | arm7-main | 176 | src/arm7/20261102_wl_receive_helpers1092/receive/ordinary_wireless.c | include-shim |
| 0x27eb90c | arm7-main | 168 | src/arm7/20261102_wl_cam_registration716/ordinary_wireless.c | include-shim |
| 0x27f172c | arm7-main | 168 | src/arm7/20261101_wl_frame_builders1304/ordinary_wireless.c | include-shim |
| 0x27f20dc | arm7-main | 164 | src/arm7/20261102_wl_interrupt_transmit1236/TxCtrl/ordinary_wireless.c | include-shim |
| 0x27ed474 | arm7-main | 160 | src/arm7/20261102_wl_mlme_tasks_timeouts860/ordinary_wireless.c | include-shim |
| 0x27ec480 | arm7-main | 156 | src/arm7/20261102_wl_cam_bootstrap292/ordinary_wireless.c | include-shim |
| 0x27f1114 | arm7-main | 148 | src/arm7/20261102_wl_transmit_family1600/TxCtrl-sp1p5/ordinary_wireless.c | include-shim |
| 0x27f1ec8 | arm7-main | 148 | src/arm7/20261101_wl_frame_builders1304/ordinary_wireless.c | include-shim |
| 0x27ea9c8 | arm7-main | 144 | src/arm7/20261102_wl_receive_helpers1092/periodic/ordinary_wireless.c | ambiguous (array in includes) |
| 0x27e8bd0 | arm7-main | 140 | src/arm7/20261102_wl_tasks_command1224/TaskInit/ordinary_wireless.c | include-shim |
| 0x27f0ce0 | arm7-main | 140 | src/arm7/20261102_wl_transmit_family1600/TxCtrl-sp1p5/ordinary_wireless.c | include-shim |
| 0x27f1b5c | arm7-main | 140 | src/arm7/20261101_wl_frame_builders1304/ordinary_wireless.c | include-shim |
| 0x27ec51c | arm7-main | 136 | src/arm7/20261102_wl_cam_bootstrap292/ordinary_wireless.c | include-shim |
| 0x27f0288 | arm7-main | 128 | src/arm7/20261101_wl_tx544/native_host_arm7_main_027eff00.c | include-shim |
| 0x27f16b0 | arm7-main | 124 | src/arm7/20261101_wl_frame_builders1304/ordinary_wireless.c | include-shim |
| 0x27eb850 | arm7-main | 120 | src/arm7/20261102_wl_interrupt_transmit1236/WlIntr/ordinary_wireless.c | include-shim |
| 0x37f8650 | arm7-wram | 120 | src/arm7/20261102_wl_tasks_command1224/TaskOps/ordinary_wireless.c | include-shim |
| 0x27f0b0c | arm7-main | 116 | src/arm7/20261102_wl_transmit_family1600/TxCtrl-sp1p5/ordinary_wireless.c | include-shim |
| 0x27f2068 | arm7-main | 116 | src/arm7/20261102_wl_interrupt_transmit1236/TxCtrl/ordinary_wireless.c | include-shim |
| 0x27f2000 | arm7-main | 104 | src/arm7/20261102_wl_interrupt_transmit1236/TxCtrl/ordinary_wireless.c | include-shim |
| 0x37fa660 | arm7-wram | 104 | src/arm7/20261102_wl_interrupt_transmit1236/WlIntr/ordinary_wireless.c | include-shim |
| 0x27e9578 | arm7-main | 100 | src/arm7/20261101_wl_parameters220/ordinary_wireless.c | ambiguous (array in includes) |
| 0x27f0c7c | arm7-main | 100 | src/arm7/20261102_wl_transmit_family1600/TxCtrl-sp1p5/ordinary_wireless.c | include-shim |
| 0x27ed410 | arm7-main | 100 | src/arm7/20261102_wl_mlme_tasks_timeouts860/ordinary_wireless.c | include-shim |
| 0x27edb20 | arm7-main | 84 | src/arm7/20261102_wl_receive_helpers1092/confirm/ordinary_wireless.c | include-shim |
| 0x27f0ac4 | arm7-main | 72 | src/arm7/20261102_wl_control_setters_key484/Key/ordinary_wireless.c | include-shim |
| 0x27e9744 | arm7-main | 68 | src/arm7/20261101_wl_parameters220/ordinary_wireless.c | ambiguous (array in includes) |
| 0x27f11a8 | arm7-main | 64 | src/arm7/20261102_wl_transmit_family1600/TxCtrl-sp1p5/ordinary_wireless.c | include-shim |
| 0x37f86c8 | arm7-wram | 60 | src/arm7/20261102_wl_tasks_command1224/TaskInit/ordinary_wireless.c | include-shim |
| 0x27ed514 | arm7-main | 60 | src/arm7/20261102_wl_mlme_tasks_timeouts860/ordinary_wireless.c | include-shim |
| 0x27ead78 | arm7-main | 52 | src/arm7/20261101_wl_parameters220/ordinary_wireless.c | ambiguous (array in includes) |
| 0x27edad4 | arm7-main | 44 | src/arm7/20261102_wl_mlme_tasks_timeouts860/ordinary_wireless.c | include-shim |
| 0x20685b0 | main | 12 | src/mechanics_save/identity_profile_pointer.c | declaration-only |
