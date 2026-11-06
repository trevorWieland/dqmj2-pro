# Word forwarding, bounds and explicit clear — 2026-11-01

This is the queued source104 package:21 new ordinary C functions covering1,838 initialized native bytes, plus two alternative44-byte implementations with zero additional coverage. Its build acceptance remains pending until its own current validation report passes. The existing ROM match still uses original-object scaffolding; neither a source-only ROM nor the full Windows game is established.

The ARM9 main identities are scoped to the measured ROM hash674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6. Every identity also carries its module, ARM mode, exact address and target/source/object hashes in the matching reports.

## Bounds and shadows

`python match_main_bounds_shadows124_20261101.py` qualifies0202AD78/44,02029D5C/40 and02029E68/40. There are1,920 original/C pairs and3,840 actual returns, using fresh ARM946 instances, protected full-page effects, frame checks and independently calculated results. Five source/output alias arrangements test ordered bound writes and32-bit wrapping. The two shadow routines truncate full-word inputs to16 bits, retain different global/MMIO store orders and return the old shadow value. The MMIO model establishes payload/store order; physical device behavior remains unproved.

Three genuinely compiled wrong-C alternatives produce177 actual returns and140 independent rejections. One-instruction exhaustion receives no return credit. The qualifier also passes from an unrelated directory under isolated Python. Trace archives preserve all cases.

## Channel and MMIO forwarding

`python match_main_word_channels340_20261101.py` qualifies seven32-byte channel wrappers, three28-byte MMIO wrappers and two16-byte in-place field rebasing routines. All3,072 original/C pairs agree with independent models of full-word arguments, the fifth stack argument, ordered external writes,32-bit arithmetic and raw return-register observations.

The corpus separates4,608 observed own-code returns from1,536 completions through supplied tail services. The5,120 supplied-service calls receive no native-helper credit. Seven C functions are declared void; observing their raw R0 does not establish a public return-value contract. The services return normally in this scope; their implementations and hardware effects remain outside it.

The three MMIO functions contain20 executed instruction bytes and two verified literal words each: the MMIO address0x04000400 and the corresponding service entry. An initial assumption of a four-byte pool was rejected and retained as failure evidence. All340 initialized bytes match genuine MWLD output; the model does not count literals as executed instructions. Twelve compiled wrong bodies generate288 independently rejected completed invocations, with216 own-code returns and72 supplied tail completions recorded separately.

## Application handoff: explicit arguments matter

`python match_mechanics_save_20261101_lane_explicit_clear.py` qualifies the192-byte caller020C5E88 and the two zero-credit alternatives020BF5C0/44 and0207CDB8/44. The caller conditionally invokes0205DF8C with explicit zero after clearing its field+0x1C. It passes the native0202A250 result into020BF5C0 and passes explicit2 into0207CDB8. The forwarded outgoing words include the supplied first word and the retained context pointer. These are measured word-level relationships; original formal types and gameplay names remain qualified.

The three-C composition and independent native executions produce7,424 top returns,59,904 native-helper returns and37,824 explicitly provided service calls. Six wrong-C controls produce62 actual returns with38 independent rejections and24 unchanged positive cases. Negative-selector prefix stops retain zero parent-return and post-fault credit.

The two forwarding alternatives also execute2,048 Windows native C calls with a supplied two-word callback. Separately compiled archival C completes another2,048 calls:1,792 non-null contexts expose the missing forwarded words, while256 null-gate contexts remain positive. This is a concrete reason to validate typed C behavior as well as ARM byte matching before using recovered routines in application adapters or a native port. The archival primaries remain preserved; only explicit source preferences may migrate after accepted build validation. No application adapter or UI was edited.

## Read-only research

The ARM7 IRQ witness reconciles nine gap entries,208 already initialized bytes and the pre-existing discontiguous ISR association. Its71 controls pass in the coordinator checkout. A versioned replay adapter permits exactly one checkout-specific missing-file diagnostic path to relocate; every frozen producer, validator, original report and all other report fields remain pinned. No namespace, fixed-word data binding or source-admission permission is granted.

The ov005 controller/Ghidra packet retains the2,328-byte native controller's2,324-byte C candidate and1,609 equal bytes,544 completed bounded invocations,2,040 supplied calls and partial2,044-byte own-instruction coverage. It earns no exact source credit. Its independent program address mapping and Ghidra exports remain hypotheses, with database stack metadata distinguished from measured native frames.

New unmodified dependency references remain explicitly hash-pinned copied inputs. They are not authored source or new tracked-dependency exceptions. The historical ten-reference materializer stays unchanged, and the unnecessary eleven-reference preparation is recorded as unadopted. A source-only fresh-checkout claim requires its own terminal validation; the older live replay is not silently relabeled.


## Additional core routines with original lower code

`python match_main_list_unlink132_20261101.py` qualifies main ARM0200B7C8/132 with1,200 original/C pairs,2,400 actual top returns and3,600 actual original IRQ-helper returns. No helper outcomes are supplied. The model covers inactive gates, optional predecessor/successor links, a shared-neighbor alias, full-word flag preservation except bit0, and the conditional global-root reset. Both IRQ/FIQ mask initial states and restored control state are checked. Three compiled wrong-C alternatives return516 times and produce192 independent rejections. The unit requires the demonstrated O2/inline-off/speed profile; its initial space-profile failure is retained rather than generalized away. All128 own instruction bytes and44 helper instruction bytes are observed; four own initialized bytes are a literal pool.

`python match_main_callback_list100_20261101.py` qualifies main ARM0202DDA0/100 with1,750 original/C pairs and3,500 actual top returns. The886 callback returns execute original shadow-setter bodies, with zero supplied outcomes and zero additional helper source credit. The independent model covers zero to four acyclic nodes, unsigned full-word selector/count comparisons, flag bit0x100, null callbacks, low-byte callback payloads, ordered shadow/MMIO writes and the caller's Boolean result. All100 caller instruction bytes and64 distinct callback instruction bytes are observed. Four compiled wrong bodies produce1,000 actual returns with136 independent rejections; the unchanged contexts remain positive. The actual callback entry words are checked even where the native test callback ignores them. Cyclic/mutating lists, physical device behavior and original callback formal types remain unproved. Both qualifiers also pass from an unrelated working directory under isolated Python.

The new Thumb020B48C8/186 source packet covers1,908 actual top returns,1,418 native-helper returns and seven explicitly supplied boundaries, including ARM/Thumb indirect callbacks and seven-word frames. Four wrong bodies return48 times with31 independent rejections and17 unchanged positives. Four supported bounded returns and four unsupported stops remain separate; stops receive no completed-return credit. The separate716-byte caller remains inexact and receives zero source credit.

The constructor509 research packet retains a full1,720-byte C candidate with1,679 matching bytes. Its16 bounded invocation completions agree on final effects and ordered writes under2,864 supplied calls. Eight raw-R3 differences are separately qualified by40 executions of the original main08C58 helper, which overwrites that incoming word before use. The caller remains inexact and receives zero source credit.


## SDK heap attributes and context initializer

The main ARM0202AE9C/424 preferred scalar C now genuinely matches every initialized byte. The SDK-shaped group macro uses explicit unsigned maskBits/newValue temporaries before its two assignments, preserving the already measured direction/alignment lifetimes. The formerly commuted ORR is resolved through source types/lifetimes, with no instruction patch, register forcing or new compiler settings. The comparative public reference and its exact revision/file hashes are pinned; equal SDK revisions, thresholds and fill behavior are not assumed. The volatile alternative remains separately labeled diagnostics.

`python validate_main_sdk_heap_attribute424_20261101.py` passes1,120 positive own returns and9,120 separate original-helper returns, with full registers/APSR, mapped memory/stack hashes, ordered reads/writes and helper arguments checked. Thirty-five metadata/availability controls and four compiled/genuinely linked wrong-C controls pass; the latter produce2,240 actual returns and1,151 independent model rejections. The old parent C/fixture remain unchanged. Original main-module reference pins remain evidence-only. An explicit committed consumer ledger names this one additional ARM9/main/address/producer identity; all existing default ARM7 namespace and source-only compiler-input refusals remain intact.

The main Thumb0209DE84/340 initializer is qualified by602 original/C pairs,1,204 top returns,34,916 original-helper returns and two explicitly supplied boundaries. Its literal-zero forwarding to0209F80C has separate original-callee prefix/connected qualification. Those80 checkpoint occurrences receive zero parent/callee return credit. Four compiled wrong bodies physically return32 times with15 independent rejections and17 unchanged positives. The source's conditional scope and supplied boundaries are retained; this does not establish a complete cold-context initializer path.

## Reproducible generated frontier

The generated recovery archive preserves564 C drafts from605 independently queued Root identities. All385 historically compilable units now compile and genuinely link again from their archived C, without historical source objects or old WORK-directory inputs. Their40,072 initialized native bytes and53 byte-exact hypotheses are research metrics, not added accepted coverage. Compiler profiles are pinned per unit across the measured1.2/base,2.0/base and2.0/sp1p5 compiler identities. The first archive replay rejected69 profiles when it incorrectly assumed the current default compiler; its complete failed report is retained. The corrected version selects and hashes each original compiler and preserves every historical exact/inexact outcome.

Generated hypotheses retain unproved types/signatures and receive zero source credit until separately qualified and accepted. New generated C paths make a single Windows git-add command49,215 characters long, so the versioned package stager uses Git's NUL-delimited pathspec input. It retains the same path/hash exclusions, frozen diagnostic classification and unchanged full oracle collector. The older stager remains preserved. The source103 input-audit display-name typo is separately resolved by verifying its recorded code hash against the actual version5 script; the frozen report is unchanged, and version6 derives its generator name from its file.


Packaging initially refused whitespace in three frozen Ghidra497 exports under `evidence/generated/`, while correctly identifying the separate Root generated archive. The exported bytes remain unchanged. The versioned stager/finisher now recognizes that exact namespace only when the current file hash matches its frozen handoff manifest and the manifest itself matches its pin. This grants zero source credit and does not waive authored-source whitespace checks. The original failed classifier output remains archived.
