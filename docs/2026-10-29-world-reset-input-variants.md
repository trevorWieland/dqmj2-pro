# World reset inputs and numeric writer effects — 2026-10-29

The original `world.e` entry 128 reaches and completes the previously measured reset helper under both synthetic numeric 0/1 values 4/0 and 13/0. This extends the earlier single-profile result without certifying a selected save bank, natural travel, actual scene resources or renewable encounters. No ordinary script source or new native body receives credit from this research.

Run `python evidence/encounter/world_reset_variants_20261029.py`. The versioned report is `evidence/encounter/world-reset-variants-20261029.json`, keyed by the original ROM/module/archive/script/code hashes and qualified native getter/setter identities. Earlier frozen trace reports and source are unchanged.

All 36 world profiles start with fourteen selected primary bits set: 346–349 and 500–509. They use identical original images, zero volatile context, persistent/register seeds and every other initial byte; only numeric slots 0/1 differ. The source/code pointers and entry 128 are installed by native initialization/start calls. No PC is forced afterward, no instruction is skipped, and the first returning yield/end/nonprogress or unsupported native call stops the prefix. The last successfully returned persistent checkpoint is saved before any failing call, and post-fault state is excluded.

| Input family | Profiles | Observed boundary/result |
| --- | ---: | --- |
| Numeric 0 = 0 through 14, or 255; numeric 1 = 0 | 16 | Reset helper returns; all fourteen bits clear before unsupported SYS104 |
| Numeric 0 = 4 or 13; numeric 1 = 1, 45, 47, 68, 70, 72 or 255 | 14 | Same supported reset result and SYS104 boundary |
| Numeric 0 = 4 or 13; numeric 1 = 46, 69 or 71 | 6 | Earlier unsupported SYS50 prevents reaching the reset helper in this context |

Thirty cases reach the call at world PC 0xC528, enter helper 32 at 0xEB48, execute its return at 0xF9E0, and clear all selected flags. Their unsupported SYS104 boundary remains PC 0xD14C, faulting at native ov000 ARM021D8728. The six special numeric-1 profiles stop before reset at SYS50, faulting at main ARM02037D1C. Their unchanged selected bits are only a pre-resource-fault checkpoint; they do not prove that a fully initialized game would fail to clear the bits.

Entry 128 reads numeric slot 0 into local 78 and slot 1 into local 79. Its explicit comparisons distinguish numeric-1 values 46, 69 and 71 before forwarding local 78 into helper 32. The helper begins clearing flags before its later argument-dependent calls. Numeric-state names such as story chapter, time of day, music selection or travel mode are not assigned by this evidence.

The world matrix and nineteen independent writer slices produce 25,312 actual native returns. Each counted call reaches the return sentinel, preserves SP and callee-saved registers, stays below 20,000 instructions and uses the existing one-second bound. Every world profile additionally has one nonreturning resource/context probe; the thirty-six failed calls are excluded from the return count. There are no native function stubs.

## Qualified numeric writes

The existing static script scan identifies nineteen constant SYS40 writes to numeric slots 0/1. Each three-instruction setter slice was independently exercised through the original native VM after explicit manual selection of that slice. All nineteen modify exactly the expected serialized numeric byte and return the previous unsigned byte as float. They total 76 true native calls including initialization. Their enclosing game paths are not claimed reachable.

| Archive | Numeric slot | Observed constant values |
| --- | ---: | --- |
| k01e02 | 0 | 4, 6, 10, 11 |
| k01e03 | 0 | 1 |
| s01e05 | 0 | 13 |
| s02e12 | 0 | 3 |
| s03e10 | 0 | 5, 7, 8, 9 |
| s08e11 | 0 | 12 |
| world | 0 | 2 |
| s03e01 | 1 | 46, 69, 71 |
| world | 1 | 0 at three distinct sites |

The native numeric get/set entries are main ARM02063B18/02063B28; RAM is 0x021C0DC8 plus index, mapping to serialized bank offset 0x393C plus index. Setter writes the low byte and returns the previous unsigned byte. The writer fixtures prime that byte to 250, then assert both the complete persistent partition and returned float 250. Native IDs, archive/script/code hashes, PCs and full traces are recorded per slice.

## Captured and synthetic contexts remain separate

The save worker independently measured pinned `inputs/save.sav`, SHA-256 `169d65a4c6ffcb0fe996d652f73a01f70d594a08ad2385098f628abbe1c4b8f0`: the first physical half has numeric bytes 13/0, while the second half has 0/0. This does not establish native bank selection or a current valid world state. The battle Runtime's partial initial copy ends at 0x393C and consequently omits the numeric/flag planes; the native deserializer and constructed-record installer preserve the full extent through 0x3A68. Those contexts can therefore differ before deliberate scenario setup.

Profile 13/0 uses those two captured byte values with otherwise synthetic state, not a captured full runtime. Profile 0/0 is likewise a controlled input and does not stand for a selected saved bank or all effects of a partial Runtime copy. The matrix shows that both pairs reach the supported reset checkpoint under its explicit setup. It neither fixes the application nor assumes the missing initial planes are harmless for other predicates.

The reset remains predicate-rearming evidence. A complete access/repeatability argument still needs the natural caller transition, actual resource initialization, map reentry/contact conditions, successful actor creation and battle/reward ordering. None is bypassed or replaced by a once-ever or unlimited-supply label here.
