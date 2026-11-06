# ARM7 halfword copy, recurrence and control source

Three complete ordinary-C units reconstruct 188 initialized bytes in two program namespaces: 168 instruction bytes and 20 generated literals. Host main `027E926C/48` copies sixteen halfwords; utility-child main `027E944C/48` performs a low16 recurrence; utility-child main `027EADB8/92` updates a control bit and conditionally transfers a halfword between disposable register addresses. All three fresh source-only builds genuinely link to every original byte. Source/module adoption is pending integrator review.

The host unit matches under the pinned 2.0/base compiler; both child units match under pinned 1.2/sp2p3. These settings are demonstrated for these units, without a general SDK/compiler-version claim. Compiler/archive identities and actual flags are pinned in `nonmatching/arm7-bulk/20261031/lane-halfword-context188-final/closure.json`. Source and the shared header are under `src/arm7/lane_20261031_halfword_context188/`.

The initial forty-function leaf campaign produced forty drafts and thirty-seven compilable functions, with no exact matches before refinement. A bounded four-profile pass found nine same-size functions and still no exact unit. The close copy draft had native two-byte post-index accesses but generated `u16 *` increments by two, doubling the byte stride. The generated control draft used byte arrays for native halfword register accesses. The recurrence draft also needed unsigned multiplication to give defined C semantics for large halfword products. The original hypotheses and measured compiler results remain zero-credit history in `evidence/attempts/arm7-halfword-historical-draft-limitations-20261031.json`.

The corrected copy uses ordinary halfword pointer increments and covers separate, identity and both forward-overlap contexts. The recurrence explicitly multiplies as u32, narrows the store to u16 and returns the native reloaded halfword as a full word. Its scenarios perform three connected state updates each. The control routine retains an unsigned full-word 0/1 guard, bit preservation and exact halfword hardware widths; larger raw input words return five without reading the context or storing data. No application/story/access/error-code meaning is inferred.

The external runtime word at `0380FFF4` lies outside the initialized/BSS module extents. The original strict linker refusal is preserved. `link_arm7_halfword_runtime_word_20261031.py` is a separately named fork permitting that exact four-byte data word only for these three full processor/program/module/mode/address/size identities and a hash-qualified producer report. General unknown-symbol checks remain intact; no BSS ownership or data-source credit follows.

The producer proof executes original host constructor `027E89EC` to its natural helper-return boundary `027E8A10`, and original child constructor `027E8B78` to `027E8B9C`. Each loads incoming descriptor word zero, stores that pointer to the runtime word and executes the real context-clear helper for 694 hex bytes. Sixteen fresh prefixes give sixteen actual helper returns and zero enclosing-constructor returns. Six independent instruction-role mutations are rejected. These are explicit caller-entry setups, without proof that enclosing initialization/thread/game flows reach them.

Existing primitive global declarations are preserved: host `extern u32 native_arm7_data_0380fff4`, child `extern u32 native_utility_child_arm7_data_0380fff4[]`, word zero only. Typed pointee views have minimum sizes 3A4 and 5F6, without a total-original-object claim. The source remains native32-bit address-word C and uses direct volatile halfword lvalues for measured device-region addresses. An Android/host-pointer portability claim is not made.

Reproduce both namespaces with Python 3.13.5:

```
python C:/Users/trevo/Documents/RecProgramming/DQM/j2p-recovery-lanes/arm7/match_arm7_lane_halfword_20261031.py
python C:/Users/trevo/Documents/RecProgramming/DQM/j2p-recovery-lanes/arm7/validate_arm7_lane_halfword_20261031.py
python C:/Users/trevo/Documents/RecProgramming/DQM/j2p-recovery-lanes/arm7/audit_arm7_halfword_transport_20261031.py
```

The matcher also accepts `--program host` or `--program child`; each regenerates its own canonical report with the exact program/module tag required by the unchanged host and utility builders. No mixed top-level namespace is published.

Positive fixtures produce 192 actual original/compiled host-copy returns and 6,080 actual child returns, with 4,352 real context-clear returns counted separately. The owned functions have no callees or lower providers. Every side starts from a fresh machine and compares all registers/CPSR, stack, mapped-memory and memory-access evidence. Independent models cover all mapped bytes, complete own writes, data-read widths/strides and full-word returns. Qualified literal-pool reads are retained in the all-read comparison and excluded only from the separate independent data-read model.

All 81 standalone controls pass, including metadata/source/ABI/namespace/return claims, current missing/corrupt products after caching, narrow runtime-word scope, and preserved original linker refusals. Three same-size wrong C bodies change copy stride, coefficient offset or hardware access width; each genuinely links and explicitly returns before independent model rejection. A one-instruction cap remains unsupported with zero return credit.

Two setup/model failures are retained: an absent guessed child extraction path was rejected before child execution, and an early independent read model omitted PC-relative literal reads. Corrected input paths come from the measured inventory; current comparisons retain all reads. Original source, executable inputs, accepted generators and shared ledgers/configurations remain unchanged.

The TI925T Unicorn model is a bounded surrogate. Original data/callees and prerequisite setup receive zero new source credit. No physical device timing, malformed-pointer portability, asynchronous/shared-memory behavior, full-program opaque-pointer resolution, ordinary scene reachability, BIOS execution or complete-game reconstruction is claimed. No emulator, audible execution, real-save mutation or application edit occurs.

Both terminal source-only replays, including the different-working-directory run, reproduce host report `500ef6fc5a5955365e11ab30382127cc0f91e5c368463f6b97422f31caeb9e28` and child report `51bdf0c90382f3d237709f99d8d52626b2f841184ec061c2134261bfebd4a5fd`. The 81-control report is `a4fd2cfb1dcc0fc8f18789d2cba60871b0011372784f466f7bd2409edc9e4df9`; the standalone zero-credit producer report is `368e444be97b6a9cd49a2eb1c0993e5c153c5073fb12dff67ebdd282f0f5bbf7`. Compiler, source, model, boundary, qualifier and verifier inputs are frozen for integrator replay.
