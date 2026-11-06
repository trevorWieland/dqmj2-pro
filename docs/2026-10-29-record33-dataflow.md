# Record byte0x33: qualified dataflow, 2026-10-29

This note adds measured copy, restoration and nonzero-writer behavior for the byte tested by the separate stock-reward guard in ov001:ARM021E4C34. The byte remains unnamed. A status, ownership, injury, permanent exclusion or reward-eligibility interpretation is not established by these experiments.

All identities use private ROM SHA-256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`. Original ROM/save files and application sources are unchanged. Overlay identities are explicit because their load addresses overlap. Each Unicorn top-level call requires an actual return, restored stack pointer and preserved callee-saved registers within 200,000 instructions. The fixtures supply no callee providers.

## Saved and transient locations

The saved record array starts at ARM9 RAM021BD674 with 132-byte records. Record byte0x33 maps to selected serialized-bank offset `0x21B + recordIndex*0x84`, following the native main-state copy from bank0x90 to RAM021BD51C.

The runtime root is RAM021C0EF4. The three local front views begin at root+0x20; the three local reserve views begin at root+0xC80. View stride is0x210. These addresses are separate from the battle flag-word root discussed in the earlier state-context handoff.

Native main:ARM020649FC, 292 bytes, copies saved record+0x20..0x3F to view+0x11C..0x13B. Thus saved byte0x33 corresponds exactly to view byte0x12F. Main:ARM02065210, 164 bytes, resolves three front and three reserve view IDs and copies the same32-byte block back. Nonzero marker values are retained without boolean normalization. The commit also transfers runtime gold and clears main-state byte0x153; the expected-state model includes both effects.

`record33-copy-20261029.json` checks four prior marker bytes against seven replacement bytes in six independent records:28 cases,392 actual native/source returns. The existing matched C bodies are freshly linked with the real MW linker before source execution. No source credit is added. Source/object/native-span/link hashes are embedded in the report.

## Qualified nonzero writer

Ov000:ARM02224700 has a configured260-byte native span, SHA-256 `2e1c53f6622874cf6e6345d39e8ed88041ca99d03c60d5ee4857e91893346875`. Its measured interface is `void transfer(int side)` over supported side values0/1. Incidental R0 contents are not a semantic return contract.

The routine first obtains context `RAM021CECF4 + side*0x170`. Mutation requires all three gates:

- Byte RAM021CEBE2 is nonzero.
- Signed context byte+0x16C equals-1.
- Word RAM021CEC04 has bit29 set.

It obtains six views through native main020895E8(side,index). Non-network local-side selection comes from u16 RAM021C72AC through the original native helper chain. Equal-side selection uses local front/reserve arrays; unequal-side selection uses the other six views. The network-mode helper branch remains unsupported by this fixture.

For each view whose signed halfword+0x2E is not-1, it copies a signed halfword pair from context+0x14C+index*4 into view+0x120/+0x122. A zero first value sets marker+0x12F to1. A positive incoming value does not generally clear an old nonzero marker. If no valid front-three view received a positive first value, a second pass writes first value1 and marker0 to each valid front-three view. Empty views are skipped; reserve values do not prevent this fallback.

`record33-zero-fixtures-20261029.json` independently models all6,368 runtime bytes and the complete saved region. It covers236 cases: both side values, both non-network local-side values, seven raw prior marker bytes, eight formations with positive/zero/negative/empty fields, and all three failing gates. Native and compiled typed C agree on472 routine returns plus2,832 native setup-getter returns, totaling3,304 actual returns. All logged writes are restricted to the three qualified fields of selected views. Saved bytes remain unchanged in this routine.

Preferred source is `nonmatching/save-core/20261029-preparation/record33_zero_value.c`, SHA-256 `551ba647e1ce08ed5d2a83dd0225166611c268e82b7ccb3025d51386321a03f4`. Its pinned-MW object SHA-256 is `b7a470555cfc4126598d052e6d1eedb2fc9daec595fe79235d560bf43ff82883`; real-linked binary SHA-256 is `6d573004c3c9ca952aa156cca87e09ee76a6e783b43b642e135333039bc96f48`. The source is276 bytes with151 same-offset native bytes and receives zero exact credit. Its temporary Unicorn injection occupies16 following bytes; no other overlay routine is invoked by the covered dependency graph. The int-index variant is268 bytes and also unmatched. Both attempts are preserved separately.

This establishes a zero-value event and front-group fallback associated with the marker. It does not identify the halfword pair as health/magic or the marker as death. Physical scene reachability, arbitrary side values, network selection and other view-kind values remain unproved.

## Temporary formation frames

Native ITCM:ARM01FF8580,132 bytes, snapshots into `RAM01FFF8A0 + frameIndex*0x48`. ITCM:ARM01FF8604,184 bytes, restores from the same two temporary frames. Six12-byte entries hold ID at+0, record+0x24/+0x26 at+4/+6, and record+0x32/+0x33 at+8/+9. Padding and stale fields are preserved when lookup fails.

Restore clears the current front/reserve ID arrays, reinserts cached IDs through the original native writers, and restores the four saved fields for successful lookups. Real reserve reinsertion retains the separately measured secondary14/15 transition behavior. These temporary ITCM frames are not physical save banks.

`record33-snapshot-20261029.json` checks both frames, seven raw marker bytes and five arrangements including holes, duplicates and unknown IDs:70 cases,140 actual native returns. Expected cache bytes and the entire expected saved region are checked. The two functions already have matched ordinary C and receive zero new credit. This report executes original native bodies and does not independently relink their C counterparts.

## Resetters and ov005 caller conditions

The existing matched ov005:ARM021E5D40,140 bytes, queries three front and three reserve records. For each nonnull record it invokes native0207B460(species,variant,record+0x7A,temporary64), stores native0207C2B8(record+0x20,temporary64) at+0x24, stores0207C3D8 at+0x26, and clears byte+0x33. `record33-refresh-20261029.json` checks42 cases and84 actual native/source returns with no callee providers. Records outside the selected formation retain their raw marker values. Derived halfwords are checked against actual native callee results rather than an independently reconstructed formula.

Three qualified direct ov005 callers are preserved with exact native-span hashes and call addresses in that report. Their following conditions are static native-instruction evidence, not full caller execution or proof of ordinary scene reachability:

| Caller | Refresh call | Conditions on the path |
|---|---|---|
|021E1CFC,420 bytes|021E1E10|Helper021E0938(1,0x11) must not return1; input-mask bit1 follows the selected branch; selector1 reaches refresh, while selector2 additionally requires primary bit285. Selector0 follows another action. Input-mask bit2 follows an earlier return path.|
|021E3398,284 bytes|021E33C4|Main020644C0 returns nonzero; caller clears ov005 state+0x18, restores temporary frame1 through ITCM01FF8604, then refreshes.|
|021E3D54,84 bytes|021E3D6C|Main020644C0 returns nonzero; caller restores temporary frame1 and then refreshes before later scene operations.|

Primary bit285 is selected-bank offset0x39B7 bit5. Main020644C0 returns1 when0207DEA8 is nonzero, but may first call020C225C(0x20000000) when0207E3F8 is nonzero. Its return1 therefore is not independently a successful-save guarantee.

Existing matched main020633C8,100 bytes, and ov003021D790C,216 bytes, contain qualified saved-record reset operations of the same fields. Their source identities are reused; this note does not add a new execution claim for them. Other instructions at offset0x33 are not assigned to this record field without pointer provenance.

## Replay and report identities

Run the following with pinned Python3.13.5. Each path resolves independently of the working directory:

```powershell
& C:/Users/trevo/AppData/Local/Programs/Python/Python313/python.exe C:/Users/trevo/Documents/RecProgramming/DQM/dqmj2pro-decomp/evidence/application/record33_refresh_20261029.py
& C:/Users/trevo/AppData/Local/Programs/Python/Python313/python.exe C:/Users/trevo/Documents/RecProgramming/DQM/dqmj2pro-decomp/evidence/application/record33_copy_20261029.py
& C:/Users/trevo/AppData/Local/Programs/Python/Python313/python.exe C:/Users/trevo/Documents/RecProgramming/DQM/dqmj2pro-decomp/evidence/application/record33_snapshot_20261029.py
& C:/Users/trevo/AppData/Local/Programs/Python/Python313/python.exe C:/Users/trevo/Documents/RecProgramming/DQM/dqmj2pro-decomp/evidence/application/record33_zero_fixtures_20261029.py
```

| Report | SHA-256 |
|---|---|
|record33-refresh-20261029.json|d763522e796f8a57a71f2a6d5b3771c7884affdbdd96bd9ebeec9a328bc6d0bf|
|record33-copy-20261029.json|b7dd861906ba4a1a4d5da7f13fd8b41bc937fec8ca3071ee7a2c35ef634ab8b1|
|record33-snapshot-20261029.json|c8ad7360a1892813300507e7354f5fbd915e6132086bd6c16fde799ad13b3345|
|record33-zero-fixtures-20261029.json|bea48a7bc22b3c635c45e1eb51e654995d4506e9f6e7bb8137c85f8d440a2e2b|

Together these reports contain3,920 actual top-level returns, including2,832 setup-getter returns. They establish bounded dataflow behavior and preserve all accepted source. Net new exact source credit remains zero. The separate stock-reward guard is not executed while ov000 or ov005 is loaded in these fixtures.

## Exact source candidate, pending integrator acceptance

Subsequent natural C lifetime changes remove the extra loop-entry branches, use a separate second-loop index, and declare the context pointer before the initialized group flag. `src/mechanics_save/20261029_record33_zero_value.c` is a byte-identical promoted copy of the resulting hypothesis, SHA-256 `05a263947298b3df6cfe03c4994408b1d19ee7235fdf58cedd5f3fb85c69c742`. Its complete260-byte body equals the native span after the real pinned MW link. No assembly, opcode patching, fake arguments or artificial return types are used.

The promoted-source object SHA-256 is `54f3dc14fb139bdaf12dedeef309e68b5cba900b157942fcac4d47600064394b`. Linked bytes have native SHA-256 `2e1c53f6622874cf6e6345d39e8ed88041ca99d03c60d5ee4857e91893346875`. Object differences from the hypothesis copy include compiler source-file metadata; text equality is independently checked. Exact link controls, validation, ELF and binary are preserved in immutable hashed artifacts referenced by the report.

The separate `record33_zero_exact_fixtures_20261029.py` verifier pins the source hash, native span, complete real link and connected native controls. It defaults to the promoted source and accepts an explicit repository-relative `--source`. `record33-zero-exact-fixtures-20261029.json`, SHA-256 `f8523742e78837ac520f3ab42451a415fe703b59902ddd8b71ab6685633d7ea7`, repeats the same236 independent model cases against original native and exact compiled C:472 routine returns plus2,832 setup-getter returns. These are additional executions of existing vectors rather than new semantic coverage. The earlier276-byte source, source verifier and report stay frozen.

```powershell
& C:/Users/trevo/AppData/Local/Programs/Python/Python313/python.exe C:/Users/trevo/Documents/RecProgramming/DQM/dqmj2pro-decomp/evidence/application/record33_zero_exact_fixtures_20261029.py --source src/mechanics_save/20261029_record33_zero_value.c
```

The explicit-source replay succeeds from an unrelated working directory with the same report hash. The candidate contributes260 prospective ordinary-C bytes only after integrator registration, real module reconstruction and whole-ROM gates; this worker does not alter shared ledgers or accepted builds. The preferred current source is the promoted exact candidate, while the earlier nonmatching files remain experiment evidence.

## Exact reader candidate and canonical replay

Main:ARM02078E3C is a separate76-byte wrapper with interface `void display(u32 recordID, int argument)`. It obtains the saved record through native02062A10, reads the raw byte+0x33, obtains a context through ov000:ARM0221744C, and calls main0206C718(context,1,argument,rawByte,0,choice). Choice is12 when the raw byte is zero and18 otherwise. The context getter reads word ov00002245334; its overlay identity remains explicit. Record IDs must resolve: this wrapper does not add an absent-record guard.

Promoted source `src/mechanics_save/20261029_record33_reader.c` has SHA-256 `bbd3c5c2134566f97f9832dc57ea9624a40837f8a0d4a36fc6648a37436baafd`; its object SHA-256 is `03c454f4e0bbf31f9cfaf55a318635310040d0e3ac86b7b574111f1a30d0d8da`. The complete76 bytes match after real pinned MW linkage.

`record33_reader_fixtures_20261029.py` accepts repository-relative `--source`, defaulting to that promoted source, and pins its hash. Its168 cases cover seven raw bytes, first/last saved-record slots, six signed argument boundaries and two context pointers. Native and exact C produce336 actual wrapper returns and the exact independently expected six-argument dispatch; the complete saved region is unchanged. One explicitly bounded UI provider substitutes main0206C718, captures four register plus two stack arguments and returns13579BDF without writes. Record lookup and the context getter remain original native code. Rendering, font resources, hardware transfers, gameplay reachability and status labels are not proved.

`record33-reader-fixtures-20261029.json` has SHA-256 `c77dfd8fdd6306445810222c886b93cb3e17570ea078fec066f6fc973b5ddd84`. Its explicit-source replay also produces that hash from the unrelated Codex working directory.

The root replay `match_mechanics_save_20261029_record33.py` invokes both frozen exact fixture generators. Canonical output `evidence/matches/mechanics-save-20261029-record33.json` contains two exact caller rows totaling336 bytes,404 model cases,808 actual caller returns and2,832 actual setup-getter returns. Native symbol entries are checked against declared function starts, module identities and complete native-span hashes. Compiler include dependencies are explicitly empty for the two standalone source files; separately hashed replay dependencies identify the tool scripts. The script performs no shared registration or build mutation.

```powershell
& C:/Users/trevo/AppData/Local/Programs/Python/Python313/python.exe C:/Users/trevo/Documents/RecProgramming/DQM/dqmj2pro-decomp/match_mechanics_save_20261029_record33.py --writer-source src/mechanics_save/20261029_record33_zero_value.c --reader-source src/mechanics_save/20261029_record33_reader.c
```

The canonical report SHA-256 is `5c304a1c6ae2d10e53f3b540e4f6e9c235e4533bf7f24730a2e99741b64783a0`. These336 bytes await coordinator registration and full module/ROM gates. They are distinct from the frozen sources reused by the earlier dataflow experiments.

## Exact menu-enable reader candidate

Main:ARM0206C2F8,208 bytes, provides another qualified record33 reader. Its complete body is recovered as `src/mechanics_save/20261029_record33_menu.c`, SHA-256 `892eb736dcefa8e12f15198ffd43971655e08ccb7728bc43fec51c7a9d22ae84`. The promoted-source object SHA-256 is `9102f27d0951ba5edc7ef271c6475d6736c04a02564e8bb6a4aaf7a4db89a8b6`. Real pinned MW linkage matches all208 native bytes. The source uses the same measured register lifetimes through ordinary declarations; no assembly, forced arguments or artificial return types are used.

The native routine derives an enabled boolean and calls main0206BE08(0,enabled). An initial0206C3C8 result0 produces disabled. Otherwise a nonzero0206C18C(2) result leaves enabled1. When that mask gate is0, the routine collects up to three selected IDs through unchanged0206BC80 and examines them in order. Zero IDs are skipped. In modes other than2, a selected valid record with byte33==0 enables the action and stops the scan. Nonzero marker bytes exclude that record from this path. No such record leaves disabled0.

Mode2 instead calls the overlay-qualified ov001021DB4B4(0,id). A nonnull entity permits the path when either byte+0x31C or byte+0x1FF is zero. That branch is exact-byte matched but not executed in this fixture. Its loaded-overlay dependency is explicit; a coincident ov000 address is not substituted.

`record33-menu-fixtures-20261029.json`, SHA-256 `977802b5b4dbfad49511b3ceff32c9f5f46d0c688fa1b5e63c934aaab8e0f83c`, checks672 model cases and1,344 actual original-native/exact-C returns with zero callee providers. It establishes the original initial gate result1 and mask gate result0, using four raw words at RAM021C4904 with mask2 clear. Four raw non-mode2 words at RAM020EDCD8, seven marker bytes and six selections cover holes, duplicate IDs and mixed zero/nonzero markers. The native15-row selection collector executes against explicitly constructed UI rows at RAM021C4A04. Selected-ID visit order and the first permitting record's early exit are independently checked.

The native enabled setter veneer0206BE08 reaches02072E7C and writes only enabled byte RAM021C5A17 plus dirty byte RAM021C5A18=1. The expected model checks the entire UI region and saved region, and the write log requires exactly those two writes. This is transient UI state; no saved byte changes. The action's visible name, ordinary menu reachability and physical rendering are unproved. Mask2-set, initial-gate-false, mode2 entities, absent IDs and malformed/oversized selections remain execution-unsupported.

The separate canonical replay leaves the earlier336-byte report frozen:

```powershell
& C:/Users/trevo/AppData/Local/Programs/Python/Python313/python.exe C:/Users/trevo/Documents/RecProgramming/DQM/dqmj2pro-decomp/match_mechanics_save_20261029_record33_menu.py --source src/mechanics_save/20261029_record33_menu.c
```

It succeeds from the unrelated Codex working directory. Canonical `evidence/matches/mechanics-save-20261029-record33-menu.json` has SHA-256 `3816e1313d9054c2ea9bab37ea35ed1b5c4e274e22ee8881978ded4f20b8e03a`, with one exact row, verified module-qualified native symbol entries, explicit empty source includes and separately hashed replay dependencies. The two canonical batches offer544 prospective ordinary-C bytes in three distinct functions, pending coordinator registration and full module/ROM gates. No status or ownership label follows from this action-specific zero-byte predicate.

## Exact connected selection gate and extended caller paths

The dependency main:ARM0206C3C8 is recovered as a separate172-byte ordinary-C body in `src/mechanics_save/20261029_active_selection_gate.c`, SHA-256 `c423660bb077805222bea9483bd1ad9474284173ac6be31a0acd39985c2d4181`. Its promoted-source object SHA-256 is `9df6e60b926c35c05c76d3683be1c131304295ab541432479fb4af5699d008db`. The measured per-unit compiler setting is pinned MW2.0/base with `-O2 -opt speed` plus the explicit ABI flags in the report. The default-space hypothesis is168 bytes; the selected complete172-byte body matches after real MW linkage. This setting is not generalized to other units.

When native0206C18C(2) is zero, this dependency returns1. Otherwise it collects selected IDs, then reads three active IDs through original02062A68. It returns1 iff some nonzero active ID does not occur among the three selected IDs, and0 otherwise. Zero active IDs are skipped. Duplicate IDs use membership rather than multiplicity. The routine does not look up record existence, and the visible action remains unnamed.

`active-selection-gate-fixtures-20261029.json`, SHA-256 `99590ad71820a2c4318c16e845fb5fe43770c7c174878dd5ba62864d91985e16`, adds384 direct native/source cases over empty, duplicate, sparse and high unsigned IDs with mask2 clear/set. Independent expected membership is checked along with unchanged complete saved/UI state. The original selection collector and active-ID getter execute without providers.

The same report adds1,008 connected208-byte caller cases, patching both exact C bodies for its source engine and retaining the original native controls for its native engine. These cover the earlier unexecuted initial-gate-false and mask2-set paths. A mask2-set selection covering every nonzero active ID disables the row. If at least one such active ID is absent from the selection, the initial gate permits and the caller's mask2-set path enables regardless of marker33. With mask2 clear, the earlier action-specific record33 predicate applies. Only the two expected enabled/dirty bytes change; saved bytes stay unchanged. Modes0/1 are used, and the mode2 entity branch remains execution-unsupported.

The report contains1,392 cases and2,784 actual top-level returns with zero providers. Its reuse of the frozen208-byte caller adds no source credit for that caller. Existing source/fixture/canonical files remain unchanged. The extra execution coverage supplements rather than rewrites their historical limitations.

```powershell
& C:/Users/trevo/AppData/Local/Programs/Python/Python313/python.exe C:/Users/trevo/Documents/RecProgramming/DQM/dqmj2pro-decomp/match_mechanics_save_20261029_active_selection_gate.py --source src/mechanics_save/20261029_active_selection_gate.c
```

Canonical `evidence/matches/mechanics-save-20261029-active-selection-gate.json` has SHA-256 `ef4c8f67f8e0afacadc0193e38efaef3f4f98c07348ca51e9a3b0a261d783794`. It contains only the new172-byte candidate, explicit verified native bindings and the reused caller evidence. The three canonical batches offer716 prospective ordinary-C bytes in four distinct functions pending coordinator gates. No shared registration or build files are changed by these replay scripts.

## Synthetic mode2 live-entity extension

The separate `record33-mode2-fixtures-20261029.json`, SHA-256 `721fc108ccf21e69c42fa798e0d75045015b4c85db4c43ec0ed825ae0f0324ac`, executes the remaining mode2 entity branch with explicit ov001 loading. Its1,152 cases produce2,304 actual original-native/reused-exact-C returns with no providers. It adds no source credit and does not alter frozen match reports or sources.

Native ov001:ARM021DB438 returns group0 entities at RAM02236F6C plus slot*0x440 for slots0..2. Native021DB508 obtains an ID through a nullable pointer at entity+0x1E8. Native021DB4B4 scans all three slots and returns the last nonzero matching entity ID. The fixtures construct disposable ID words separately from saved records. Their presence establishes the lookup's memory contract, not an ordinary scene/save-to-entity construction path.

The independent model covers null backreferences, zero/unknown IDs, reversed slots and duplicate IDs with the last matching slot winning. Both raw flag bytes+0x1FF/+0x31C vary through0,1,128,255. A found entity permits the caller when either byte is zero; two nonzero bytes exclude it. Selected-ID order and first permitted entity's early exit are checked through actual lookup return pointers. Only enabled/dirty UI bytes change. Complete saved and entity regions are unchanged.

Saved-record33 is set to0 or255 independently. Neither changes the mode2 outcome, and original saved-record lookup02062A10 is never invoked on this covered branch. This distinguishes the qualified live-entity predicate from the non-mode2 saved-record predicate without assigning a status/ownership meaning. Mask2 is clear in this matrix; the earlier connected fixture separately covers mask2-set and initial-gate-false paths. Physical rendering, visible action name, gameplay reachability and ordinary entity construction remain unproved.

```powershell
& C:/Users/trevo/AppData/Local/Programs/Python/Python313/python.exe C:/Users/trevo/Documents/RecProgramming/DQM/dqmj2pro-decomp/evidence/application/record33_mode2_fixtures_20261029.py
```
