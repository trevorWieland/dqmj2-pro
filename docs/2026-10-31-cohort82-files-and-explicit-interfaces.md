# Cohort 82 files and explicit interfaces

The accepted build measures 8,933 matched functions and 667,629 initialized module bytes out of 2,512,636: 26.5708602440%. Six functions add 976 bytes relative to cohort 81; two explicit interface migrations add zero coverage. Unresolved initialized coverage is 1,845,007 bytes. These counts include literals and data; executable-only and overall-game completion remain unproved. The measured plan is [cohort 82](../evidence/verification/cohort-2026-10-29-82.json).

The additions are main file-size helper 0202A8E0/116, overlay000 cleanup217/232, and overlay006 ordered218/120, buffer228/112, status235/144 and prepare236/252. Their bounded native/source proofs distinguish actual helper returns from supplied SDK completions. File-size validation follows the measured input path in R0 and a complete 72-byte local record. The status helper preserves exact equality with one rather than treating every nonzero value as true. The preparation helper uses the measured unsigned word comparison.

Ordered218 retains a false preliminary comparison in its frozen raw report. A separate [linking-stage adapter](../reproduce_ov006_ordered218_linked_20261031.py) independently validates source/object/link artifact identities and all 120 linked bytes. The guard and original producer are unchanged.

Main 02041800/20 now exposes the measured raw unsigned byte. Main 0209BC38/36 sequences the producer before reading its output as a later argument, removing the prior C argument-order dependency. The two old source/object versions remain preserved, and preferences rise from 28 to 30. Neither migration adds bytes or functions. Every other prior selected source and object remains identical.

The [pointer-boundary addendum](2026-10-31-pointer-producer-boundary-addendum.md) corrects one limitations sentence without changing cohort-82 pins: both frozen overflow controls stop on logical fold reads at 0209BEB8. A separate new experiment supplies a producer write stop at 0209F702. The producer can safely return a count larger than its 32-byte backing when its disabled prefix causes no copy; the later fold can still exceed its readable extent. These synthetic bounds do not establish an import restriction, original handled error or console fault.

The regression driver passes all 20 module comparisons, two checksum matches, 36 vectors with 144 isolated actual returns, 5,117 getter comparisons and the exact scaffold-assisted ROM. The ROM remains 175,959,612 bytes with SHA-256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`. Original inputs and the baseline remain unchanged. Outside application edits keep strict whole-workspace isolation false.

Immutable checkout X is replaying frozen cohort 81 plus the batch/static-input packaging repair; its success is not yet asserted. A full clean replay of cohort 82, complete source-only ROM construction, full Windows game execution and Android device execution remain unproved. The 40,560 semantically unknown save bytes remain unknown.

Reproduce with `python run_cohort_20261031_82.py` followed by `python finalize_cohort_20261031_82.py`, using absolute script paths from another working directory. Preparation verifies old selections and the exact six-function/976-byte delta before publication. The accepted plan also records both zero-coverage migrations.
