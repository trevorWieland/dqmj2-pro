# Slot kind normalization and helper inputs

Main ARM `02046188` now has a genuine 236-byte ordinary-C match under its unchanged historical Metrowerks 2.0/base compiler and flags. Its 216 executable bytes and 20 literal bytes match after real MWLD linking. Integrator registration/module acceptance remains separate.

The source is `src/mechanics_save/20261101_lane_slot_kind/native_main_02046188.c`, SHA-256 `23ac5f9caf0684833332841563bc1d13013dd7a20f7468517cf53a5799a7738c`. It retains the native ARM32 address view and measured 20-byte slot stride. Names and the bounded probe backing do not establish the original array extent.

The old unsigned-byte formal caused the compiler to assume incoming R1 was already normalized. It omitted the native `ANDS R0,R1,#255`. The preferred source takes a raw word, stores its low byte at slot offset `10`, assigns a separate word selector `arg1 & 255`, and switches on that value. A byte local remained at 225/236 matching bytes; the word local naturally matched all 236 without opcode edits, assembly, fake arguments or register constraints.

Every invocation first writes zero words at slot `8` and `C`. Normalized kind one conditionally initializes both slot words `0` and `4`; kind two conditionally initializes only word `0`; all other kinds take the default word-zero path. The four measured helper routes are:

| Kind/path | R0 descriptor address | R1 selector | R2 | R3 |
|---|---|---:|---|---|
| Kind one, word zero absent | `020DDAB0` | 0 | Incoming third word | Address of slot `8` |
| Kind one, word four absent | `020DDAC8` | 1 | Incoming third word | Address of slot `C` |
| Kind two, word zero absent | `020DDAE0` | 16 | Incoming third word | Address of slot `8` |
| Default, word zero absent | `020DDAF4` | 15 | Incoming third word | Address of slot `8` |

The helper's raw R0 is stored into the corresponding word `0` or `4`. The function returns the final full word at slot `8`, independently of that supplied handle word. No success-boolean or resource-size interpretation is assigned.

## Evidence and scope

`python match_mechanics_save_20261101_lane_slot_kind.py` rebuilds the declared source/object/link, executes the native and linked functions against an independent field/call-order model and emits `evidence/matches/mechanics-save-20261101-lane-slot-kind.json`.

The matrix has 2,464 contexts and 4,928 actual original/C returns. It exercises all 256 low kind bytes with four upper-word patterns, plus initial nonnull words, raw zero/high-word returned handles, zero/high-word in/out field values and declared callback side effects. It records 2,756 supplied helper calls and zero original helper returns. All own instructions execute. Fresh machines, complete register/flag/read/write comparisons, callee-saved/control/SP restoration, stack guards and full slot/neighbor memory checks are required.

`020451C4` is supplied in these executions. Its actual native prologue separately corroborates all four inputs: R0/R1/R2/R3 are saved to R8/R7/R6/R5. Native conditional `LDRNE R7,[R5]` at `02045284` and `STRNE R7,[R5]` at `020452A0` establish that the fourth word is an in/out pointer on the corresponding path. These sites and the complete 360-byte callee identity are pinned. The helper's full file/archive/allocator behavior, original formal declaration and enclosing scene reachability remain unproved here.

The supplied callback can explicitly change the future word-four gate, overwrite the current word before the constructor stores returned R0, or change primary word `8` during the second call. These synthetic side effects prove fresh reads/overwrite order in the constructor; they do not claim the original helper makes those extra mutations. Caller registers and flags are legally clobbered at each verified external BL.

A complete compiled wrong-C body removes only the normalization. Six original/wrong pairs actually return: three independent rejections for high-word special kinds and three causal positives for low-only kinds or a default high-word kind. No fault or timeout counts as a rejection.

The synthetic index-eight guard control stops at an explicitly checked logical write boundary with zero return/post-fault credit. Tested indices 0/1/7 and this backing limit do not imply an original public capacity or import restriction.

Full per-case evidence remains in deterministic gzip with content hashes. Canonical replay rebuilds every object and consumes no scratch golden. The separate 141 compiler experiments and failed byte-local hypothesis remain as research, with zero credit. Earlier source, matches, application, ROM/save and unknown-byte accounting remain unchanged.
