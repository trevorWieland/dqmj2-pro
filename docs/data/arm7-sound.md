# ARM7 sound structures

Index entries: `arm7_player_view`, `arm7_track_view`. Confidence: **proven-by-code** for
the fields and strides (both sizes are asserted in the matched sources), **unknown** for the
record count.

These live in ARM7 WRAM (`0x0380_0000` region), so they are **not ROM tables**: they only
exist once the sound driver has initialised. A dump of a ROM image cannot contain them;
`public_tools/data_dump.py` rejects them for that reason.

## Player block — `0x03808420`

| offset | width | type | name | confidence |
| --- | --- | --- | --- | --- |
| 0 | 1 | u8 bitfield (`NativePlayerFlags`) | flags | proven-by-code |
| 1 | 1 | u8 | playerId | proven-by-code |
| 8 | 16 | u8[16] | tracks | proven-by-code |
| 24 | 12 | u8[12] | reserved18 | unknown |

`NativePlayerFlags` is a one-byte `u8` bitfield (`typedef struct NativePlayerFlags { u8 active : 1; ... }`),
so `flags` is 1 byte and `playerId` sits at offset 1. The same file asserts
`sizeof(NativePlayerView) == 36`, which proves the stride.

Evidence: `src/arm7/20261030_seq_init/native_arm7_wram_037ffef0.c` (function `native_arm7_wram_037ffef0`),
`src/arm7/20261030_seq_main/native_arm7_wram_037fff54.c`,
`src/arm7/20261030_seq_public/native_arm7_wram_038002f0.c`.

## Track initializer — `0x03808660`

| offset | width | type | name | confidence |
| --- | --- | --- | --- | --- |
| 1 | 1 | u8 | panRange | proven-by-code |
| 4 | 1 | u8 | volume | proven-by-code |
| 5 | 1 | u8 | expression | proven-by-code |
| 6 | 1 | s8 | pitchBend | proven-by-code |
| 7 | 1 | u8 | bendRange | proven-by-code |
| 8 | 1 | s8 | pan | proven-by-code |

Evidence: `src/arm7/20261030_seq_access/native_arm7_wram_03801884.c` (function
`native_arm7_wram_03801884`, declares the full `NativeTrackInitializerView`) and
`src/arm7/20261030_seq_neighbors/native_arm7_wram_03800aa8.c` (function
`native_arm7_wram_03800aa8`, declares a `NativeTrack` view of the same address). That file also
asserts `sizeof(NativeTrackInitializerView) == 64`, which proves the stride.

The file's own typedef continues past `pan` with `extPan`, `extFader`, `extPitch`, envelope
fields, `priority`, `transpose`, portamento fields, `sweepPitch`, `channelMask`, `wait`,
`base`, `current`, a 15-byte reserved tail, `callStackDepth` and `head`. Those are
declared but not indexed here: the two matched views disagree on the reserved layout, so
listing them as table fields would overstate what is proven.
