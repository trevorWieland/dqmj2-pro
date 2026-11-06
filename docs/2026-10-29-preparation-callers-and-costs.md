# Preparation callers, eligibility and costs, 2026-10-29

Ordinary preparation uses separate eligibility, commit and scene stages. The measured allocation commit updates an existing skill and library state; a different ordinary item-use caller can teach a new skill and debit a book. The application currently guards and invokes the existing-skill allocation commit directly. Full scene access and future item acquisition remain separate prerequisites.

Reproduce `python evidence/application/preparation_fixtures_20261029.py` and `python evidence/application/preparation_trace_20261029.py`. The stable first fixture report is `evidence/application/preparation-fixtures-20261029.json`, SHA-256 `5de49273a0c8a6b0182022b640c731f56ede5b6febad0e1070eac69a6e939803`. Its generator and machine-source hashes, native source/object/link identities, complete vectors, writes, meaningful calls, real asset hashes and limits are recorded inside it. `nonmatching/save-core/20261029-preparation/index.json` distinguishes preferred domain hypotheses from reused matching providers and a retained incorrect m2c input. All work is private; application files were read only and accepted source was preserved.

## Allocation entry and ordinary caller

All entries below are ARM9 main, ARM mode. `02076D70` has a complete124-byte native span and a measured `void f(s16 delta)` interface. It stores the low16 delta in transient scratch, reloads it with signed extension, then performs this sequence:

1. Call `02062F3C(record.id, (s8)selectedSlot, delta)` to add to the allocated-point byte. The writer returns0 when ID lookup fails, but this commit does not inspect that result.
2. Call `02078978` to rebuild transient features and actions from the selected record.
3. Subtract the signed scratch delta from the selected record's `+3C` halfword, storing the wrapped16-bit result.
4. Call `0207AEBC(species, skillId, allocatedByte)` and clear menu byte `+2D1`.

The commit contains no free-SP, point-cap, inventory or price check. Direct execution accepts negative deltas and byte/halfword overflow. It still debits the selected pointer's free-SP halfword when ID lookup fails and the allocated-byte writer returns0. Those are bounded malformed/raw-context observations, not ordinary gameplay permissions. Valid selected-pointer/ID agreement, slot0..4, a nonnegative affordable delta and the skill's capacity must be established by its caller.

Its ordinary direct caller is `02076DEC` (1,000 bytes), reached from state6 of `0207726C`. At call `020770D8`, it commits a reached threshold minus the saved slot allocation. At `020770F8`, it calls the frozen36-byte helper `02076D4C`, which returns signed16 `(menu.goal - currentPair[1])`, then commits that remaining difference. The surrounding UI advances threshold/feature/evolution messages. Main-to-overlay UI calls carry unresolved loaded-overlay and ordinary scene-reachability prerequisites.

The276-byte bound calculator `020768D8(output8, cursor)` reads the selected skill's threshold table and signed free-SP halfword. It fills three signed halfwords and two equality flags. It bounds the proposed value by current allocation plus free SP and raises the lower edge to the current allocation. Its callers initialize/update the goal before confirmation; raw invalid SP can produce an invalid interval. It performs no saved-state write. Cursor0..10 and slot0..4 are the tested table/index domains; arbitrary aliases and out-of-range cursors are unproved.

## Field and persistence map

Saved-record locations below are relative to a132-byte record. For record index `n`, serialized bank address is `0x1E8 + n*0x84 + fieldOffset`. This is RAM state destined for serialization; these tests perform no device or save-file write.

| Field | Width / behavior |
| --- | --- |
| Record `+14` | Physical ID,32 bits; the writer looks this up independently |
| Record `+18`, `+1A` | Signed species halfword and variant byte |
| Record `+3C` | Stored16-bit free SP; these native calculations sign-extend it |
| Record `+7A+2*s`, `+7B+2*s` | Skill ID byte and allocated-point byte, five slots |
| RAM `021C6420` | Transient selected-record pointer, menu `021C6234+1EC` |
| RAM `021C6330` | Word-valued selected slot, menu `+FC` |
| RAM `021C6484` | Signed32 target allocation, menu `+250` |
| RAM `021C651A` | Transient signed delta scratch, `021C6434+E6` |
| RAM `021C6505` | Transient menu byte `+2D1`, cleared by commit |
| RAM `021C6424..021C6464` | Derived feature list,64 bytes; rebuilt from current record |
| RAM `021C6464..021C6484` | Derived action bit set,32 bytes |

Library observation is persistent RAM behavior beyond the record's own point fields. Existing matching `0207AEBC`,188 bytes, marks the skill observed, raises its packed stage count when appropriate and records attained feature IDs. Native category2 returns early unless primary state bit16 is true; other categories proceed. The serialized roots are feature bits `36F8` / RAM`021C0B84`, skill-observed bits `3718` / RAM`021C0BA4`, and packed stage nibbles `3738` / RAM`021C0BC4`. Names describe measured storage, not complete quest meanings. A zero delta can still update this library state and transient derived/menu state.

Existing matching `02078978`,64 bytes, calls feature collection `0207B460`, then action filtering `0207B1C4`. It refreshes transient buffers and does not itself spend items or gold. Existing matching `02062F3C`,56 bytes, returns lookup success and adds directly to the selected byte without clamping or checking slot capacity. All those providers are reused; no duplicate source credit is claimed.

## Ordinary skill-book path

Main `020731AC`,968 bytes, is an ordinary selected-item caller. In the measured single-target mode, ItemTbl byte40 equal to `1A` selects the skill-book branch. The selected item is a signed halfword at RAM`021C61FC`; the low nibble at `021C61FE` selects this mode. The selected-record pointer comes from the word-indexed pointer array at `021C6210`, with selected index at `021C5B20`.

It takes the low byte of ItemTbl halfword `+1C` as the new skill ID, rejects a duplicate through `02062F74`, counts existing nonzero skill IDs through `02062EE4`, and compares that count against `02062F2C(species)`. That capacity helper returns native category plus3. If space exists, `02062E44(id, count, &pair)` writes the new ID with allocated points0 and invokes the existing skill observer. No free SP is spent by this teaching operation.

The ordinary outer UI `020735F8` reaches this caller from state3 after confirmation, an exit-row check, a selected-row enable-byte check and a special-item-ID42 diversion. Source ordering is established; the complete menu population, positive-quantity gate and loaded scene have not been proved. A synthetic zero-inventory invocation still grants the skill and clamps the attempted debit at zero. A synthetic hole in the skill list makes the nonzero count identify an occupied slot, overwriting that slot. Ordinary use therefore needs positive owned quantity and the expected compact skill-list invariant before invoking this local caller.

On success, `02065DEC(item)` compares ItemTbl byte37 (`+25`) against unchanged native `RNG(100)`: consumption occurs only when the byte is greater than the draw. If true, `020630E4(item,-1)` debits the signed inventory byte, capped/clamped by its native item logic. Rejected duplicate/full-slot cases perform no draw or debit. All26 measured book rows in this modified build have byte37 equal to100, so each successful tested book use consumes one. This is a property of these hashed rows; it does not turn the general consumption helper into an unconditional rule.

Measured book item IDs are `48..57`, `74..79`, `84`, `244..249`, `252..254`; the fixture records each mapped skill ID and real table hash. Their per-item capacity byte39 is99. Inventory byte `i` maps RAM`021BD558+i` to bank`CC+i`. Native add/debit uses signed byte storage and clamping. No saved-gold change occurs in these book vectors or allocation vectors. Shop purchase, paid services and access to an item source are outside this proof; it establishes no free item supply or general absence of fees elsewhere.

## Preferred hypotheses and validation

The three preferred ordinary C hypotheses cover1,368 genuinely unmatched native bytes. They remain outside recovery and earn zero exact credit:

| Source under `nonmatching/save-core/20261029-preparation/` | Native / compiled bytes | Same-offset bytes | Native/source evidence |
| --- | ---: | ---: | --- |
| `allocation_commit.c` | 124 / 132 | 56 | 540 cases,1,080 returns |
| `allocation_bounds.c` | 276 / 264 | 73 | 1,980 cases,3,960 returns |
| `item_use.c` | 968 / 964 | 331 | 130 book cases per engine,260 returns |

All5,300 successful executions reach the return sentinel within200,000 instructions; each execution starts fresh, with registers and stack reset, restored SP/callee-saved registers required, and writes restricted to declared state/scratch/stack/division regions. Independent models check the whole serialized RAM region for allocation, exact8-byte bound output and unchanged saved state for bounds, and exact book record/debit/return behavior. Native/source saved-state hashes, meaningful argument/call traces and RNG division traces agree. Stack-pair addresses and unused caller-saved registers are not required to match across nonmatching C frames.

Allocation cases cover all five slots, both primary16 states, three raw EKT category representatives, successful/missing ID lookup and boundary/negative SP deltas. Those include malformed states and reserved table rows; they do not establish legal gameplay records. Bounds cases cover skill22, all five slots, cursors0..10, multiple goal/allocation/free-SP values and negative signed-halfword interpretations. Book cases use species1/category0, single-target mode, every measured book row, ordinary/duplicate/full/zero-inventory/hole contexts. Other item branches and modes remain unsupported.

Allocation/bounds run unchanged native dependencies without function substitution. Book fixtures substitute exactly five UI/display entries: overlay0 `02215698`, `02215BC8`, `021E7B9C`, and main `0205F35C`, `020756E4`. They return bounded zero values and provide no gameplay arithmetic, inventory or skill mutation. Division registers have a bounded nonnegative numerator/positive denominator provider. Native RNG state updates, inventory mutation, slot initialization and skill/library routines execute unchanged. These substitutions cannot certify complete scene reachability.

The retained m2c input for `020731AC` has source SHA-256 `ef477501c01c3ccbd784ccafe393933edf72f5006e762823e6685bfeafcfb154`. It treats a pointer-array load as a byte, reads a word index as a byte, assumes two independent stack bytes are a contiguous pair, and uses undefined `NULL`. The preferred source supplies an explicit pointer load, word index, two-byte aggregate and pointer-return declaration; it passes the bounded book domain. Those are source-inspected defects and a compilation failure, not a claimed legacy execution counterexample. Non-book branches and complete Android64 ABI translation require separate proof. Compiler/linker equality and module/regression gates remain mandatory before any hypothesis replaces accepted source.
