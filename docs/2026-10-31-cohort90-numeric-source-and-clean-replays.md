# Cohort 90: numeric source, Windows execution and clean replay ordering

The accepted cohort measures 9,010 native functions and 679,219 source-linked initialized bytes out of 2,512,636 inventoried bytes: 27.032128808152077%. The unresolved extent is 1,833,417 bytes. These totals include pools/data and are not an executable-only or overall game completion percentage. A source-only ROM and complete Windows game remain unproven.

The [acceptance receipt](../evidence/verification/cohort-2026-10-29-90.json) and [driver](../evidence/verification/cohort90-validation-driver.json) measure three new functions and 720 bytes. All previous selections and 61 explicit preferences are preserved. All 20 module comparisons, both checksum helpers, 36 vectors/144 isolated returns and 5,117 getter comparisons pass. The 175,959,612-byte output retains the required ROM SHA-256 using remaining original executable scaffolding. Baseline and original input hashes remain unchanged; strict workspace isolation still detects external application edits.

## New source

Main ARM 0203B660/416 uses its demonstrated 2.0/base O3 inline-off speed profile. A named unsigned quotient recovers the actual multiplication/shift lifetime. Seventeen preserved C/profile trials yield one genuine complete linker match. Its 640 recipe pairs produce 1,280 caller returns, 7,764 original helper returns and 4,224 supplied lower-service entries. All 404 instruction bytes and 12 literal bytes are checked. [Native qualification](2026-10-31-main-numeric-dispatch-native-qualification.md) records supported paths, ordered effects and supplied boundaries.

The same source compiles separately to an ordinary PE32 Windows program: 640 actual source returns, 3,882 supplied C-helper calls and 2,112 lower-service calls pass the synthetic page expectations. A whole-C wrong transient value returns normally and is rejected. A zero-payload COFF symbol object supplies absolute addresses without instruction/data credit. An asInvoker manifest resolves the retained initial WinError740 launch failure without elevation or policy changes. This proves one source unit. [The Windows record](2026-10-31-numeric-dispatch-native-windows32.md) contains hashes, commands and limitations.

Main ARM 02089390/196 checks signed-positive IDs, exact validation result 1 and independent group sums greater than 3. Its 896 top returns include 5,166 actual helper returns and 3,850 supplied validation entries. Actual lower policy, asset ranges, scene reachability and party/import meaning remain unproven.

Main ARM 0206D274/108 is the sequence adapter: 496 top returns and 8,432 original constructor/SDK returns use no supplied calls. Pointer-table words, signed sentinel behavior and wrapping byte state are measured. Unsupported slot/context/index cases remain separate stops. A constructor's stack-derived field does not establish lifetime after return.

## Clean replay repair

Checkout X failed because a proposed ARM7 validator checked a historical work object before its producer ran. Checkout Y was stopped after confirming the same defect in its immutable snapshot. Neither was repaired in place or given cached work objects.

Two new wrappers create fresh work directories, invoke each unchanged producer, then invoke its unchanged validator. Root passes 36 historical controls and 4 additional checks per wrapper, including missing-object rejection before and after a fresh run. Proposed/duplicate source receives zero new credit. [The replay record](2026-10-31-arm7-clean-proposed-and-duplicate-replays.md) retains hashes and audit limits. Cohort 90 registers these wrappers instead of the cache-dependent direct validators.

A new complete clean checkout must use committed cohort 90 plus verified source/oracle closures. Its result remains pending until every command finishes; earlier clean cohorts do not prove this cohort reproducible.

The imported sequence fixture retains its hash-pinned blank line at EOF. The dedicated whitespace receipt records this one frozen-input exception; authored whitespace checks otherwise pass with CRLF recognized.

## Reproduction

Run `python run_cohort_20261031_90.py` then `python finalize_cohort_20261031_90.py` for integration. Run `python check_main_numeric_dispatch_windows32_20261031.py` for the Windows C unit. The source registry freezes individual producers; `python reproduce.py` retains the checksum entry point. No application, adapter, UI, public remote or external messaging is changed.
