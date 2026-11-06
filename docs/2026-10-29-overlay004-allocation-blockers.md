# Overlay004 allocation blockers and independent codec evidence — 2026-10-29

This handoff adds zero accepted functions and zero matched executable bytes. The four remaining ordinary C bodies are drafts. Existing accepted sources, frozen matches, shared registries and build code were not edited. Recovery rotates to overlay000 after this bounded investigation.

## Frozen drafts and byte comparisons

| Entry | Draft | Native span | Closest equal bytes | Profile |
| --- | --- | ---: | ---: | --- |
| ARM9/ov004/ARM/021D8410 | `src/overlays/ov004_20261029_cart_draft.c` | 576 | 555 | Pinned MWCCARM2.0 SP1p6, O4 speed, inline all |
| ARM9/ov004/ARM/021D8650 | same unit | 576 | 555 | same measured profile |
| ARM9/ov004/ARM/021D8B00 | `src/overlays/ov004_20261029_codec_encrypt_draft.c` | 280 | 267 | Pinned MWCCARM2.0 base, O4 speed, inline all |
| ARM9/ov004/ARM/021D8C18 | `src/overlays/ov004_20261029_codec_decrypt_draft.c` | 392 | 366 | Pinned MWCCARM2.0 base, O4 speed, inline on/noauto |

Each comparison normalizes only declared ELF relocations. No register renaming is normalized. The encrypt mismatch is an R5/R6 allocation exchange; decrypt exchanges the current pointer and offset in R4/R8. The cart pair retains three allocation cycles involving sector/buffer and control/address values. SP1p6 fixes an additional scheduling difference seen with base; its improvement is not transferable to other units without measurements.

The cart draft corrects the 020102C4 declaration and call to pass the acquired lock identifier, as demonstrated by the accepted main-runtime implementation. This correction changes no emitted instructions because R0 already contains that identifier. Both cart variants differ in their measured factor choices and final multipliers. Their MMIO paths were not exercised by the new codec probe. No genuine linker acceptance is claimed for any draft.

## Independent execution evidence

Run from any working directory:

```powershell
python "C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\probe_overlay004_codec_state_20261029.py"
```

The driver requires Python3.13.5 and Unicorn2.1.4. It validates the measured ROM namespace, independently decrypts/re-encrypts the original stored overlay, compiles the two frozen drafts with pinned compilers and executes native analysis bytes against entry-substituted draft bytes. The three callees at021D7DE8,021D8A70 and021D8AC8 execute their original native implementations. No host-call stubs replace those callees. Every call must return within100,000 instructions and may access only the own image/BSS and bounded private64KiB stack. Executed PCs are further restricted to the selected entry and those three helper spans.

The new reference model tracks a mutable1024-byte arena and the complete268-byte state, including32-bit feedback, both indexes and all256 table bytes. It covers disjoint buffers, in-place operation and aligned partial overlaps of−16,−4,+4,+16 bytes; branch/BL/BLX/ordinary instructions; duplicate table entries; arbitrary initial index bits; feedback boundaries; zero lengths; low and high-bit-set invalid lengths; and poisoned pointers when those arguments are unused. Input mutations made by instruction category are compared, including decrypt's source-word mutation after output stores.

All528 vectors/1,056 executions agree with the independent model on return values, complete state/arena and native R0–R15/CPSR. The two targets execute355,638 instructions per native/draft side,711,276 total. All264 encrypt vectors also agree on full stack, ordered value-bearing writes, executed addresses and instruction counts. Only129/264 decrypt vectors agree on the full machine effects:135 retain differences in nested native helper saves of the draft's differently allocated R4 value. Those private scratch-stack differences are recorded rather than discarded. This is a behavioral draft result, not a byte match.

Latest report: `work/overlay004-recovery/20261029/native-state14/behavior-fe5e0bfd1a78e1a1a8c23d754a594b217b7b75fec7c33994f97ea119bac5ad06.json`. Driver SHA-256: `67852145d331ed2260230e0c599e61ae85da2502c746896ad038cf874c79ef19`. Native analysis SHA-256: `e2f3984c4d3ce460fd78cd1afff59746047d590b50eab9b320b211cab369bde0`. Compile reports inside that evidence freeze source/object/compiler hashes, actual commands, relocations and both nonmatching byte strings. Earlier reports and the initial stricter full-stack failure log remain preserved.

## Negative experiments and alignment limits

All experimental files are under `work/overlay004-recovery/20261029`. The bounded debug comparison tests sym off/on on the closest human C under base and SP1p6; code remains identical. Standard register hints, declaration order, byte-helper parameter order, switch scopes/order, C++ linkage, word/union scratch storage, const byte reads and disjoint-state hypotheses do not resolve the remaining allocations. All384 documented optimizer-option profiles across both codecs and the cart pair produce zero full-byte matches. Profile result arrays include failures and the actual compiler output; failed options are not silently adopted.

The two codec wrappers reserve288 bytes, so they preserve incoming stack alignment; both codec prologues reserve296 bytes, preserving eight-byte ABI alignment. No stronger32-byte stack alignment is asserted. Local inverse-table alignment4/8 adds code and worsens the match. State.table's known four-byte layout alignment alone gives no improvement. There are no external data symbols in the codec bodies to strengthen by a measured global address.

Selected retained profile counts: `{"cart-p6-retarget11": 95, "debug-lifetimes10": 8, "decl-perms08": 720, "helper-params15": 36, "map-storage18": 48, "switch-shapes13": 32, "valid-options16": 384}`. Other retained directories preserve ABI, long-type, source-context, pointer-birth and compiler-cross checks. These are unsuccessful research results and contribute no decompilation percentage.

## Continuation constraints

Keep the22 DSProtect shim templates unaccepted as assembly: an independently recovered template does not prove original vendor assembly. Preserve the accepted narrow CP15 justifications and all prior C/source-runtime proofs. Do not count the native helper bodies, analysis-image substitutions, disassembly or this successful behavioral comparison as new reconstructed source. Hardware, interrupt, exception, unaligned-pointer and source/state-alias paths are outside the new fixture domain; portable signed-overflow semantics are not asserted. The measured frozen compiler behavior is what was tested.
