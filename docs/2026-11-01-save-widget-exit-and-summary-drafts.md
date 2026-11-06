# Save widget exit and larger summary drafts

Main ARM `02079F9C` now has a genuine 36-byte C match, with 32 executable bytes and one four-byte literal. Source `src/mechanics_save/20261101_lane_save_widget_exit/native_main_02079f9c.c` has SHA-256 `ee0fe8d3f3bc4cfc368a58db05ded8d7d819c7e26319105160631dd684cadbfc`. It preserves the measured historical Metrowerks 2.0/base profile and real MWLD relocations. Registration and shared module/ROM gates remain integrator-owned.

The original contains an explicit comparison with mode eight after the mode-one branch. The old m2c if-expression removed this empty case and generated only 28 bytes. A normal C switch with cases one and eight naturally restores the exact body. No fake inputs, padding, assembly, register constraints or opcode changes were used.

Mode one passes singleton `021C6638` into original overlay-zero ARM `022163A4`, measured extent 88 bytes. Other mode words make no helper call. The source retains a raw word view of physical R0: incoming mode on other paths, final helper R0 on mode one. Known main call sites overwrite or ignore that result; no public return meaning or complete caller-consumption claim follows.

## Returning executions

`python match_mechanics_save_20261101_lane_save_widget_exit.py` rebuilds the source and actual linked body, then compares native and compiled execution against an independent call/return/memory model.

The positive matrix has 1,536 contexts, 3,072 actual original/C outer returns, 256 separately counted original overlay-helper returns and 14,720 supplied calls. It covers full mode words, counts 0/1/2/3/7/15/63/127 and zero/high-word callback results. All 32 own code bytes and all 88 helper code bytes execute. Fresh machine state, actual bounded return, restored SP/callee-saved/control state, stack guards, complete native/source register/flag/read/write/call equality and widget/neighbor invariance are required.

The loaded overlay identity and base `021D7240` are explicit. Main `02049AD0` and overlay-zero `022162C0`/`022172DC` are supplied with verified actual call edges, input words and legal caller clobbers. The helper performs the original signed-byte counter/index arithmetic and word-half count reads. Those callbacks' real context lookup, destruction, refresh, pointer validity and scene prerequisites remain unproved.

Signed index aliases when adding five to larger loop indices are retained exactly. They do not establish an original valid context table extent or a UI count limit.

A complete wrong-C mode-dispatch body has eight actual original/wrong returns: two independent rejections and two causal positives. No failure, timeout or cycle is counted as a returned control.

## Separate nonreturn evidence

Counts 128, 255 and 65,535 are separate original-native probes under stationary supplied callbacks. Each reaches an identical complete register/control/stack/tracked-memory state at the same native loop PC with period 256. The probe stops on this explicit state repetition, rather than an instruction cap. These three contexts have zero actual outer or helper returns and zero post-stop source credit.

The count is reread inside the original loop. Mutable original callbacks, count changes or other live context could alter behavior. This is a qualified cycle under the declared providers, not a claim that an ordinary save screen hangs.

## Larger compile-first work

The adjacent `020798B8` renderer and `02079D6C` setup remain zero-credit source hypotheses. A previously failed 1,204-byte renderer now has a complete compilable C draft after two measured repairs: the text scratch is a real 60-byte object from the original seven-by-eight-plus-four clear loop, and the missing `0204A154` stack words at `02079A70` are exactly 2 and 0 from original stores at `02079A58`/`02079A60`. The coordinate pair is also a real four-byte object.

The renderer links at 1,244 bytes under the default profile and 1,256 under speed, against 1,204 native bytes. The 560-byte setup links at 556 with the proper pair; a separate pointer-lifetime view gives 568. These failures and ordinary-C hypotheses are preserved without source credit. Call-site auditing shows both known main renderer calls ignore R0; a separately retained void view remains nonmatching. No artificial coordinate-address materialization was introduced to fill the gap.

This family displays a temporary saved-header snapshot. It does not itself choose banks or serialize payloads. Preserved accepted `7979C` calls `7DF2C(0,021C65A8)`, and summary base `021C65D0` equals that header destination plus `28`. The accepted serializer/summary sources establish this dataflow; a separate header bridge will qualify native validity and field mappings. Header validity must remain distinct from full payload validity, physical bank mapping, boot fallback and chronology arbitration.

An initial canonical metadata attempt passed all execution producers but used an empty data-symbol cache. Its matcher and failure are archived under the 142 metadata-attempt paths; the final verifier reuses the already measured main module. No source, native behavior or fixture change was needed.

All earlier source, application, original ROM/save and unknown-save-byte accounting remain unchanged. Full positive, control and cycle evidence remains in deterministic gzip; canonical replay materializes its own compiler/link outputs and consumes no scratch golden.
