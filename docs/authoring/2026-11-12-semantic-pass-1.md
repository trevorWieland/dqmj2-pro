# Semantic pass 1: naming the most-called functions in ov000, ov001 and ov006

2026-11-12, branch `codex/semantic-pass-1`, base `e0baf9dd0`.

This is the first bounded pass against the project's explicit understanding debt:
a function that reproduces its bytes but is still called
`native_ov006_021fb384` with unnamed parameters is only half-done. The pass
ranks the three closed modules by caller count, derives meaning from callers,
callees, literals and tables, renames what the evidence supports, and records
what it does not.

## Result

* 14,374 `.c` files parsed; 13,597 measured function symbols; 6,234 functions
  with at least one direct caller.
* Top 40 functions ranked by distinct caller files, then size.
* 29 functions renamed, with 29/29 still byte- and relocation-exact.
* 17 files moved to semantic names; 12 definitions in lane-verified directories
  kept their `native_...` filename so pinned lane fixtures stay valid.
* 1,654 changed C files compile; 1,654 passed, 0 failed.
* 11 of the top 40 remain address-named because the evidence does not support a
  name, or because the row does not compile to its measured extent.

## Method

The call graph is static. For every `.c` file under `src/` the pass reads the
defined symbol and its address, then counts `bl`/`blx` targets in transcribed
assembly and direct C calls. Targets are resolved by address within the calling
module (overlays share a load base, so an address alone is not globally unique).
The rank is **distinct caller files**, then function size. The top of the list is
engine surface: the 72-byte record predicate `021DB8D0` has 425 caller files, the
12-byte main-loop callback setter `021F52CC` has 297, and the four-table record
selector `021DB438` has 198.

Each candidate was read against:

* its callers: what they pass, what they test on return, whether they skip on 0;
* its callees: service calls, callback installation, shared formatters;
* its literal pool: MMIO addresses named from the NDS I/O map, data tables,
  magic constants and table strides;
* its typed neighbours and lane documents under `docs/authoring/`;
* the overlay image for the bytes behind a table pointer or text reference.

Names are mechanism-level where the game concept is not proven. The pass does not
invent menu, species or battle meanings from a suggestive branch.

## Ranked call graph

`owner` is the primary definition file. The last column is the disposition in this
pass.

| # | module | address | bytes | callers | owner | disposition |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ov001 | 0x021db8d0 | 72 | 425 | `src/runtime/ov001-null01/native_ov001_021db8d0.c` | RENAMED `ov001_record_is_active_021db8d0` |
| 2 | ov006 | 0x021f52cc | 12 | 297 | `src/transplants/ov006-reuse01/native_ov006_021f52cc.c` | RENAMED `ov006_main_loop_set_callback_021f52cc` |
| 3 | ov001 | 0x021db438 | 124 | 198 | `src/runtime/root-linear-20261029-ov001/native_ov001_021db438.c` | RENAMED `ov001_side_slot_record_021db438` |
| 4 | ov001 | 0x02224050 | 84 | 141 | `src/ov001/p12_ov001_close/arm/ov001/native_ov001_02224050.c` | RENAMED `ov001_pick_random_candidate_02224050` |
| 5 | ov001 | 0x02226cb0 | 40 | 141 | `src/ov001/p8_ov001_pass1/native_ov001_02226cb0.c` | RENAMED `ov001_first_candidate_02226cb0` |
| 6 | ov001 | 0x02226bdc | 212 | 138 | `src/ov001/p12_ov001_close/arm/ov001/native_ov001_02226bdc.c` | left address-named |
| 7 | ov001 | 0x02223fe8 | 56 | 138 | `src/ov001/p10_ov001_pass3/native_ov001_02223fe8.c` | RENAMED `ov001_clear_free_candidate_slots_02223fe8` |
| 8 | ov000 | 0x02215698 | 12 | 100 | `src/transplants/ov000-reuse01/native_ov000_02215698.c` | RENAMED `ov000_display_context_02215698` |
| 9 | ov006 | 0x021e3cd8 | 12 | 93 | `src/transplants/ov006-reuse01/native_ov006_021e3cd8.c` | RENAMED `ov006_forward_four_args_021e3cd8` |
| 10 | ov006 | 0x021e3cd4 | 4 | 93 | `src/transplants/ov006-reuse01/native_ov006_021e3cd4.c` | RENAMED `ov006_noop_021e3cd4` |
| 11 | ov006 | 0x02203188 | 24 | 92 | `src/overlays/ov006_ov006-scalars02_11b592e7398b.c` | left address-named |
| 12 | ov006 | 0x021e3f28 | 44 | 84 | `src/ov006/p4_021d7240/ov006_menu_helpers.c` | left address-named |
| 13 | ov006 | 0x021ff6d4 | 24 | 80 | `src/overlays/ov006_ov006-scalars02_3ef992ea8e4d.c` | left address-named |
| 14 | ov001 | 0x02224570 | 204 | 76 | `src/ov001/p12_ov001_close/arm/ov001/native_ov001_02224570.c` | RENAMED `ov001_filter_highest_priority_candidates_02224570` |
| 15 | ov006 | 0x022031a0 | 136 | 69 | `src/ov006/g1_ov006_sweep2/thumb/ov006/native_ov006_022031a0.c` | RENAMED `ov006_display_blend_start_022031a0` |
| 16 | ov001 | 0x021dbcbc | 52 | 68 | `src/runtime/ov001-drafts01/native_ov001_021dbcbc.c` | left address-named |
| 17 | ov000 | 0x02223c54 | 12 | 67 | `src/transplants/ov000-reuse01/native_ov000_02223c54.c` | RENAMED `ov000_context_02246600_02223c54` |
| 18 | ov001 | 0x021f14a4 | 28 | 66 | `src/runtime/ov001-drafts01/native_ov001_021f14a4.c` | RENAMED `ov001_clear_state_flag4_021f14a4` |
| 19 | ov001 | 0x021f1354 | 164 | 65 | `src/ov001/p12_ov001_close/arm/ov001/native_ov001_021f1354.c` | RENAMED `ov001_begin_state_transition_021f1354` |
| 20 | ov006 | 0x022053b8 | 156 | 65 | `src/ov006/g1_ov006_sweep1/arm/ov006/native_ov006_022053b8.c` | left address-named |
| 21 | ov006 | 0x02205454 | 28 | 65 | `src/runtime/ov006-drafts01/native_ov006_02205454.c` | left address-named |
| 22 | ov006 | 0x02205470 | 16 | 65 | `src/transplants/ov006-reuse01/native_ov006_02205470.c` | left address-named |
| 23 | ov006 | 0x021e65a4 | 28 | 58 | `src/runtime/ov006-drafts01/native_ov006_021e65a4.c` | RENAMED `ov006_active_state_value_021e65a4` |
| 24 | ov001 | 0x022187dc | 160 | 57 | `src/ov001/p12_ov001_close/arm/ov001/native_ov001_022187dc.c` | RENAMED `ov001_any_active_slot_compare_022187dc` |
| 25 | ov001 | 0x021dbd30 | 12 | 56 | `src/runtime/ov001-drafts01/native_ov001_021dbd30.c` | RENAMED `ov001_record_field_1f2_021dbd30` |
| 26 | ov001 | 0x021f1438 | 108 | 53 | `src/runtime/ov001-drafts01/native_ov001_021f1438.c` | RENAMED `ov001_select_mode_id_021f1438` |
| 27 | ov000 | 0x0221794c | 80 | 53 | `src/runtime/ov000-drafts01/native_ov000_0221794c.c` | RENAMED `ov000_poll_change_notify_0221794c` |
| 28 | ov006 | 0x021e9148 | 172 | 51 | `src/ov006/g1_ov006_sweep1/arm/ov006/native_ov006_021e9148.c` | RENAMED `ov006_commit_mode_transition_021e9148` |
| 29 | ov001 | 0x02223f20 | 40 | 51 | `src/ov001/p8_ov001_pass1/native_ov001_02223f20.c` | RENAMED `ov001_count_candidates_02223f20` |
| 30 | ov000 | 0x02223c60 | 12 | 51 | `src/transplants/ov000-reuse01/native_ov000_02223c60.c` | RENAMED `ov000_context_02246600_02223c60` |
| 31 | ov001 | 0x021f949c | 60 | 50 | `src/runtime/ov001-drafts01/native_ov001_021f949c.c` | left address-named |
| 32 | ov001 | 0x0221873c | 160 | 47 | `src/ov001/p12_ov001_close/arm/ov001/native_ov001_0221873c.c` | RENAMED `ov001_all_active_slots_compare_0221873c` |
| 33 | ov001 | 0x021db530 | 72 | 47 | `src/runtime/root-linear-20261029-ov001/native_ov001_021db530.c` | RENAMED `ov001_mode_byte_021db530` |
| 34 | ov001 | 0x021eec7c | 252 | 45 | `src/overlays/ov001_20261030_effect_resource_constructor_74c8a98915b2.c` | RENAMED `ov001_effect_resource_create_021eec7c` |
| 35 | ov001 | 0x021d9494 | 56 | 45 | `src/runtime/ov001-drafts01/native_ov001_021d9494.c` | left address-named |
| 36 | ov006 | 0x021f2390 | 16 | 43 | `src/overlays/ov006_ov006-scalars02_c46d26a09399.c` | RENAMED `ov006_context_byte_16_021f2390` |
| 37 | ov000 | 0x021e07b8 | 28 | 42 | `src/transplants/ov000-reuse02/native_ov000_021e07b8.c` | RENAMED `ov000_saved_world_position_get_021e07b8` |
| 38 | ov006 | 0x02203c08 | 22 | 42 | `src/runtime/linked-near-20261029-ov006/native_ov006_02203c08.c` | RENAMED `ov006_clear_buffer_02203c08` |
| 39 | ov000 | 0x021e7b9c | 20 | 41 | `src/runtime/ov000-drafts01/native_ov000_021e7b9c.c` | left address-named |
| 40 | ov001 | 0x02202360 | 20 | 41 | `src/runtime/ov001-drafts01/native_ov001_02202360.c` | RENAMED `ov001_table_f0_entry_02202360` |

## Renamed set

Each row's justification is the shortest statement the evidence supports; the
full evidence and remaining-unknown text is in the file header.

| address | new symbol | what it is | callers |
| --- | --- | --- | --- |
| `021db438` | `ov001_side_slot_record_021db438` | Returns the 0x440-byte record for one of four sides and one of three slots. | 198 |
| `021db530` | `ov001_mode_byte_021db530` | Returns one of four mode bytes from the ov001 global 0x022355E4 in the order 3,2,0,1. | 47 |
| `021db8d0` | `ov001_record_is_active_021db8d0` | Predicate: a battle record is active and selectable. | 425 |
| `021dbd30` | `ov001_record_field_1f2_021dbd30` | Returns the signed 16-bit field at record + 0x1F2. | 56 |
| `021e07b8` | `ov000_saved_world_position_get_021e07b8` | Copies the saved-world position to an optional output and returns its address. | 42 |
| `021e3cd4` | `ov006_noop_021e3cd4` | Empty function: four-byte return-only body. | 93 |
| `021e3cd8` | `ov006_forward_four_args_021e3cd8` | Four-argument forwarder to main function 0x020273C8. | 93 |
| `021e65a4` | `ov006_active_state_value_021e65a4` | Returns state word +0x44 only while state word +0x40 equals 1, otherwise 0. | 58 |
| `021e9148` | `ov006_commit_mode_transition_021e9148` | Commits a mode transition: updates the selected mode field, clears the pending flag and returns success. | 51 |
| `021eec7c` | `ov001_effect_resource_create_021eec7c` | Creates an effect resource: acquires a handle, applies a category-based flag word and binds the actor. | 45 |
| `021f1354` | `ov001_begin_state_transition_021f1354` | Starts a guarded state transition: sets state bit 2, issues a 4-argument service call and two mode callbacks. | 65 |
| `021f1438` | `ov001_select_mode_id_021f1438` | Maps modes 0/1/2 to service ids 4/5/6 and forwards every other value unchanged. | 53 |
| `021f14a4` | `ov001_clear_state_flag4_021f14a4` | Clears bit 2 (value 4) in the ov001 state object's +0x18 word and returns the new word. | 66 |
| `021f2390` | `ov006_context_byte_16_021f2390` | Returns the signed byte at +0x16 of the context pointed to by 0x0221C008. | 43 |
| `021f52cc` | `ov006_main_loop_set_callback_021f52cc` | Installs the per-frame callback in the ov006 main-loop context. | 297 |
| `02202360` | `ov001_table_f0_entry_02202360` | Returns the address of entry index in the 0xF0-stride table at 0x0223A25C. | 41 |
| `022031a0` | `ov006_display_blend_start_022031a0` | Starts a display blend/fade on the main or sub BLDCNT register and schedules its completion callback. | 69 |
| `02203c08` | `ov006_clear_buffer_02203c08` | Obtains a buffer from 02203BD8 and clears size bytes of it. | 42 |
| `02215698` | `ov000_display_context_02215698` | Returns the ov000 display/layout context at 0x022459B4. | 100 |
| `0221794c` | `ov000_poll_change_notify_0221794c` | Polls a service, detects a change in object +4 and posts one of two notifications. | 53 |
| `0221873c` | `ov001_all_active_slots_compare_0221873c` | Returns 1 when every active record satisfies the selected comparison, 0 otherwise. | 47 |
| `022187dc` | `ov001_any_active_slot_compare_022187dc` | Returns 1 when any of three active records satisfies the selected comparison. | 57 |
| `02223c54` | `ov000_context_02246600_02223c54` | Returns the ov000 work context at 0x02246600. | 67 |
| `02223c60` | `ov000_context_02246600_02223c60` | Returns the ov000 work context at 0x02246600. | 51 |
| `02223f20` | `ov001_count_candidates_02223f20` | Counts the non-zero entries of a three-word candidate set. | 51 |
| `02223fe8` | `ov001_clear_free_candidate_slots_02223fe8` | Clears the candidate word for every one of three records that 021DB8D0 reports as inactive. | 138 |
| `02224050` | `ov001_pick_random_candidate_02224050` | Picks a random occupied slot from a three-word candidate set and clears the rest. | 141 |
| `02224570` | `ov001_filter_highest_priority_candidates_02224570` | Keeps only the candidate slots whose 022244A0 priority equals the maximum. | 76 |
| `02226cb0` | `ov001_first_candidate_02226cb0` | Returns the index of the first non-zero entry of a three-word candidate set. | 141 |

## What the renamed families actually are

Three families carry most of the value.

**ov001 candidate selection.** `02223FE8`, `02224570`, `02224050`, `02226CB0` and
`02223F20` all operate on the same 12-byte, three-word block. Callers initialise
the block from a static table, clear entries for inactive records, add record
priority, keep the maximum, pick one at random and return the first index. This is
a battle candidate pipeline, not five unrelated utilities. `021DB8D0` is its
record predicate and `021DB438` its four-side record table.

**ov006 main-loop context.** `021F52CC` installs the callback that
`src/overlays/ov006_20261031_loop212/loop.c` invokes once per frame on
`0x0221C06C + 12`; `021E3CD4` is the no-op callback used when nothing is
installed; `021E3CD8` forwards four arguments to `0x020273C8`.

**ov006 display control.** `022031A0` writes main/sub `BLDCNT`
(`0x04000050`/`0x04001050`) and schedules `02203228` as its completion callback;
`02203188` reads the same display context (`0x0221C180 + 0` or `+0xC`), and
`02203C08` clears a buffer obtained from `02203BD8`.

## Rename mechanics and verifier constraints

The address stays in every new symbol and file name, for example
`ov001_record_is_active_021db8d0`. That is deliberate, not a naming preference:
`public_tools/repo_build.py:pair_functions()` pairs a compiled symbol to the
private ledger row by the eight-hex address when the source path is not the
recorded `sourceUnit`. Removing the address would silently leave the renamed row
unmatched under the pinned private ledger. The address is also kept in the file
header comment.

Two filename classes exist:

* **17 files moved** to semantic names. Their `config/source_units.json` exact
  path rules were updated; the two that had one are `021DB438` (p003) and
  `021F52CC` (p032). The p032 move is material: without it the renamed file falls
  back to the ARM directory rule and no longer reproduces the 12 Thumb bytes.
* **12 definitions kept their `native_...` filename** because the lane verifier
  keys off it: `ops/verify_ov001_pass3.py` hardcodes the packet filenames and
  `ops/verify_asm_chunk_scan.py` globs `native_<module>_*.c`. Those files still
  got the new symbol, parameters and header; only the filename is frozen.

All source references were rewritten by exact identifier token: extern
declarations, `bl`/`blx` targets and C calls. `ops/` fixtures and hardcoded
verifier relocation tables were rewritten with the same token map, so the pinned
lane expectations name the same addresses. The public `accepted-functions.json`
snapshot was not regenerated: it is a frozen private-input snapshot, not a build
input for the repository-source path used here.

## Verification

The verifier is the project's own measurement path, not a text check:

```
python public_tools/source_units.py --root . --check
python work/semantic-pass-1/measure.py --source <each renamed file> ...
python work/semantic-pass-1/compile_changed.py
python work/semantic-pass-1/controls.py
```

* `source_units.py --check`: 0 unresolved source files.
* Renamed definitions: 29 selected, 29 compiled, **29/29 exact**, 0 unresolved
  relocations. Each selected extent equals the ledger size and every byte matches
  the module image after relocation patching.
* Changed callers: 1,654 C files compiled, 1,654 passed, 0 failed.
* Negative controls: one mutated body per renamed function, **29/29 controls**.
  A control passes when the same compile-and-compare path stops matching. The
  control set includes structural mutations (return-value replacement, predicate
  flip, a store inserted into the no-op) because several rows carry their only
  constant in a relocation addend, which the relocation patch intentionally
  replaces from the image. See `work/semantic-pass-1/controls.json` for the
  recorded result.

The private bundle available in this checkout is older than the report quoted in
the task: its ledger has 11,660 matched rows, not 14,113. Ten of the renamed rows
(`021F1354`, `0221873C`, `022187DC`, `02223F20`, `02223FE8`, `02224050`,
`02224570`, `02226CB0`, `021E9148`, `022031A0`) are `functionMatched:false` in
that pinned ledger but reproduce their measured bytes exactly. They were accepted
on the byte/relocation comparison, which is the stronger and current test; the
stale flag is noted rather than trusted. `021E3F28` is the one row where both
checks disagree with a rename: the source compiles to 28 bytes against a 44-byte
measured row, so it was left address-named.

## Functions left address-named and why

Ten of these remain address-named because the missing evidence is specific, not
"needs more work"; `021E3F28` is a verification failure, not a semantic one.

| address | bytes | callers | what is known | what is missing |
| --- | --- | --- | --- | --- |
| `02226bdc` | 212 | 138 | Copies a 45-byte table from 0x0222E920, loops 45 times, tests a 45-entry bitmap through 02218368, formats through the 45-way 02226764 dispatch and writes a 12-byte block. | The table's domain and the meaning of the 12-byte output are unresolved. Needs runtime capture of the block at a known call site, or identification of 0x0222E920/0x022435C8 in the text VM data. |
| `02203188` | 24 | 92 | Selects display context 0x0221C180 or +0xC and returns byte +9. | Nothing in the callers names the +9 field or the two contexts. Needs a caller that uses the value as a mode, or runtime observation. |
| `021e3f28` | 44 | 84 | Publishes `entry[1]` from table 0x0220795C + index*8 to 0x0220D104 and tail-calls `entry[0]`; callers pass 15/17. | Semantics are known (handler-table dispatch) but the row does not verify: source compiles 28 B, measured row is 44 B, ledger `functionMatched:false`. Needs lane repair and a fixture, not a name. |
| `021ff6d4` | 24 | 80 | Calls 02039B20(`*(u32*)0x0221C14C + 0x94`, 0, arg0). | The context object at 0x0221C14C and the callee's argument schema are unknown. |
| `021dbcbc` | 52 | 68 | Sums signed halfword +0x21C with 0207C2B8(arg+0x1EC, arg+0x1E8+0x46) and clamps to 9999. | The clamped quantity's identity (stat total? damage?) and 0207C2B8's contract are unknown. |
| `022053b8` | 156 | 65 | Eight-call UI/render sequence with constants 13, 23, 2, 1 and tables 0x0220BBD0/0x0220BBD8. | None of the eight callees is named; the sequence could be panel open, render submit or scene setup. Needs names for 021E6488/021EB9A4/021EB1B0/021E81E8/021E92B0/021E7824. |
| `02205454` | 28 | 65 | Thunk to 021E8FC0(2, 0x0220BBD8, arg0). | The 021E8FC0 service and its `2` selector are unknown. |
| `02205470` | 16 | 65 | Calls 021E9008 and 021E6494. | No evidence what the pair resets; both callees are address-named. |
| `021f949c` | 60 | 50 | Calls 0205E7A8(-1, arg0) unless arg1 != 0 and 0205ECB8(arg0, 0xA) != 0. | 0205E7A8 and 0205ECB8 are both unnamed; the 0xA flag and the -1 sentinel are unexplained. |
| `021d9494` | 56 | 45 | Calls 02042464(arg0, 020430B4(arg0->0x16A)[arg1].+4, arg2) and stores arg1 at +0x1E4. | The table returned by 020430B4 and the two callers' semantics are unknown. |
| `021e7b9c` | 20 | 41 | Wrapper for 0205E7A8(-1, arg0); callers pass 0x52/0x53/0x55/0x56. | Could be sound, message or event dispatch; 0205E7A8 is not identified. Needs one named caller or a runtime trace of the four ids. |

## Next pass

1. **ov001 candidate pipeline.** Capture the 12-byte block at
   `02224050`/`02224570` entry and exit in an emulator to name the candidate
   value (skill, item or action) and the 45-entry table.
2. **ov006 UI services.** Name the 02039B20 / 0203D294 / 0205E7A8 / 0205ECB8 /
   02042464 families; those names unlock about 700 caller sites across the three
   modules.
3. **021E3F28 lane repair.** The 28-vs-44-byte mismatch is a source-form problem,
   not a naming problem. Fix the row, then apply the already-derived
   `ov006_handler_table_dispatch_021e3f28` name.
4. **Roster record schema.** The 0x440-byte record predicate and the four side
   tables still lack a documented field map; a runtime capture of one record
   would let `+0x31C`, `+0x31E`, `+0x31F`, `+0x1F2`, `+0x1FF` and `+0x24C` be
   named from use rather than offsets.
