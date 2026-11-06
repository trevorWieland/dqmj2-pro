# Native encounter predicate/reset handoff, 2026-10-29

Fourteen primary bits guard original map-script spawn regions and are cleared by the original world reset helper in the measured build. Native execution now proves these resettable predicates under explicit synthetic contexts. It does not certify encounter access or renewable supply, and it provides no reconstructed C or assembly credit.

The immutable ROM is 175,959,612 bytes, SHA-256 674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6. Every inspected archive and the battle table is compared byte-for-byte with its FAT/FNT range in that ROM. Native image hashes and processor/module/address/mode entries are embedded in the reports. Application sources and its earlier renewability note were consulted read-only; reproduction has no application or scratch-directory dependency.

The [VM component report](../evidence/encounter/vm-state-20261029.json) records 625 actual returns. The [script guard report](../evidence/encounter/guard-paths-20261029.json) records 4,223 actual returns and two separately retained unsupported fault probes. All counted calls reach the return sentinel, preserve SP and callee-saved registers, and obey instruction bounds. Independent scenarios get fresh Unicorn machines; intentional state sequences and the explicitly copied successful pre-fault persistent snapshot are identified. There are no native function stubs.

The [static inventory](../evidence/encounter/guard-inventory-20261029.json) independently reproduces 341 member-zero SCR programs, 11,802 SYS 0A spawn calls and 24 unresolved enemy constants. It finds 6,357 narrow read/compare/branch slices and 7,898 state-write calls. Another 280 archives have non-SCR BMD0 members; no unexplained parser failure remains. These counts describe original bytecode analysis, not recovered source or available encounters. A positive scouting coefficient alone does not prove ordinary battle eligibility.

**Concrete flag predicates.** Each listed guard reads its primary bit, compares with zero and uses native opcode 1038 to skip a syntactic spawn region when the comparison is false. Actual local SYS 42 slices set the bit; actual world entry-128 execution clears it; subsequent native guard slices change back to their clear-state branch. Other entries or conditions may affect source execution. The serialized mapping follows the [save-state handoff](2026-10-29-save-state-context-handoff.md).

| Primary bit | Bank byte/bit | Map | SCR read / branch PC | Local set PC | World clear PC | Native enemy IDs in fallthrough region |
| --- | --- | --- | --- | --- | --- | --- |
| 346 | 0x39bf bit2 | s02e05 | 11914 / 1194C | 13FD0 | F08C | 77 |
| 347 | 0x39bf bit3 | s02e09 | 131E8 / 13220 | 21630 | F0C4 | 77 |
| 348 | 0x39bf bit4 | s03e01 | 1AB40 / 1AB78 | 39AA0 | F0FC | 182 |
| 349 | 0x39bf bit5 | s03e06 | 13F5C / 13F94 | 1F520 | F134 | 182 |
| 500 | 0x39d2 bit4 | s04e11 | 1A7D0 / 1A808 | 1C840 | F16C | 771 |
| 501 | 0x39d2 bit5 | s04e13 | 1BF40 / 1BF78 | 201C0 | F1A4 | 771 |
| 502 | 0x39d2 bit6 | s05e03 | 10D30 / 10D68 | 1A404 | F1DC | 771 |
| 503 | 0x39d2 bit7 | s05e07 | 11DE0 / 11E18 | 2395C | F214 | 771 |
| 504 | 0x39d3 bit0 | s06e04 | 146D0 / 14708 | 1AC74 | F24C | 771 |
| 505 | 0x39d3 bit1 | s06e05 | 13D40 / 13D78 | 1C118 | F284 | 771 |
| 506 | 0x39d3 bit2 | s07e06 | F3DC / F414 | 15A00 | F2BC | 772 |
| 507 | 0x39d3 bit3 | s07e11 | D2A4 / D2DC | E0A8 | F2F4 | 772 |
| 508 | 0x39d3 bit4 | s08e02 | F3FC / F434 | 12600 | F32C | 772 |
| 509 | 0x39d3 bit5 | s08e08 | F374 / F3AC | 11CA8 | F364 | 772 |

Primary getter/setter dispatch is ARM9 main 0205A65C SYS 41/42 -> main 02054980/020549D4 -> main 0203D0CC/0203D0D8 -> main 02063B40/02063B60. The bit array starts at RAM 021C0E20, serialized bank 0x3994. These identities are distinct from secondary flags and save-bank selection.

**The flag-500 writer has an observed caller predicate.** In s04e11, the real native entry dispatcher ov000 021E4E9C initializes entry 128 at SCR 0x1C400. Its STORE at 0x1C40C copies imported context slot 0 into local 78. Later, the conditional at 0x1C7A8 requires local 78==1. SYS 93 at 0x1C7CC reads the signed enemy triplet through main 02053E2C ->0205BD60; the first slot must equal 771 before SYS 42 at 0x1C840 sets primary 500.

Native main 0205BD6C writes that triplet at RAM 02102E14. The fixture invokes this actual setter before the actual entry dispatcher. Native ov000 021E4DEC derives context 1 only from raw entry reason 1 at RAM 02102DC0 and main 02027400 mode 2 at RAM 020EDCE0. All36 reason/mode/enemy combinations run the complete map-entry prefix without skipped instructions. Enemy771 in a companion slot does not satisfy the first-slot condition. Mode 4 imports context 2 and does not take the writer. No win, capture or loss label is assigned to those raw values here.

The supported s04e11 prefix stops before SYS 5 at SCR 0x1CFD0. A separate diagnostic attempt records an unmapped byte read at 0xA2, native main 0201D6A0. No failed-call output or post-fault state is used as proof. Other persistent effects from the executed prefix are retained as byte changes rather than suppressed.

**The reset is reached through original world-script calls.** With declared synthetic numeric[0]=4, numeric[1]=0, deterministic other persistent bytes, the selected bits initially set, and zero volatile context apart from original images/VM setup, native VM initialization main 0204BC08 and entry start main 0204BD00 run actual world.e entry 128. It calls entry 32 at SCR 0xC528 ->0xEB48; that complete helper returns through 0xF9E0 to 0xC534. The selected bits clear during the supported prefix of 834 steps. The outer map engine and world-specific entry dispatcher are not executed in this world profile.

The supported world prefix stops before SYS 104 at SCR 0xD14C. A separate attempt records an unmapped word read at 0x4C, native ov000 021D8728. This remains an unresolved outer context path, not successful entry completion. The physical travel route into world.e and a complete battle/reentry/re-spawn cycle are still unproved. These measured resets rule out assuming these bits are permanent one-time locks; they do not establish unrestricted renewal.

**Additional native contracts.** SYS 39/40 use the numeric-byte getter/setter. SYS 220 calls secondary setter02063C00 and preserves its input argument slot rather than returning the previous bit there. A rising secondary bit also sets index + 64 and primary 76; clearing it preserves those companion bits. SYS 268/269 read/replace the full 32-bit word at RAM 021BD670/bank 0x1E4. Their signed-float conversion is measured for finite bounded inputs, with no boolean normalization or clamp. NaNs and overflowing conversions remain unsupported.

Native STORE types 0/1/3 address context offsets0x50/0x10/0x450. Opcodes1039..1044 implement the six measured finite-float comparisons;1037/1038 branch on the context condition byte. Native actor-state gate ov000 022109B8 rejects byte states 4, 10, 11. Actual SYS 0A rejection fixtures demonstrate the group-byte comparison at RAM 022385B8 and a full 48-slot actor pool at RAM 02238634, stride0x2C4. Rejected construction leaves persistent state unchanged; that fact alone says nothing about later encounter renewal.

All three scripts below passed when invoked by absolute path from the parent DQM directory. Paths resolve from their files. The generator dependency closure and hashes are in each report.

```powershell
python evidence/encounter/vm_state_20261029.py
python evidence/encounter/guard_scan_20261029.py
python evidence/encounter/guard_paths_20261029.py
```

The remaining proof obligations are to bind raw return reason/mode values to named native outcomes, supply the missing SYS 5/SYS 104 context from actual resources, execute complete relevant entry paths, establish ordinary actor contact, and replay a complete encounter/return/travel/reentry cycle. The application's finite quota remains planning policy. No application adapter or UI was edited, and original executable/bytecode scaffolding earns zero source credit.
