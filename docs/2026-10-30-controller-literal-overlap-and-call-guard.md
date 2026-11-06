# Controller literal overlap and call guard

The preferred main ARM controller at`020735F8` compiles to3604 bytes,20 beyond the native3584-byte function ending at`020743F8`. The entire excess is literal data. This is established from the exact ELF ARM mapping symbols: `$a` covers offsets0..3560, and `$d` covers3560..3604, corresponding to literal addresses`020743E0..0207440C`. There is no later code mapping.

The immutable object SHA-256 is `57be4a52146dc9b8e901eef372d6fa59cfcef5e113616452439143fca70f441c`; raw linked candidate SHA-256 is `a597827107c7c394751ac53b954335ff6d5372e01dcf732378e01e65ba3ed9d9`. Neither the source, header, raw object/body nor native golden was changed to add the guard.

| Candidate address | Linked word | ELF qualification | Example candidate literal load |
| --- | --- | --- | --- |
|`020743F8`|`021C6210`|R_ARM_ABS32 data relocation|`02073868`|
|`020743FC`|`021C6208`|R_ARM_ABS32 data relocation|`02073900`|
|`02074400`|`021C5C10`|R_ARM_ABS32 data relocation|`02073A6C`|
|`02074404`|`021C5D00`|R_ARM_ABS32 data relocation|`02073B8C`|
|`02074408`|`00000FF7`|scalar literal within `$d`|`020740CC`|

`evidence/application/controller_overlap_guard_20261030.py` checks the object/body hashes and mapping coverage before installing the guard. Any instruction execution anywhere in candidate `$d` data fails. Reading those addresses as data is allowed. Reaching the overwritten original function entry`020743F8` also always fails; the guard never supplies a return value or skips the function.

Before classifying an entry hit as an external call, the guard checks the actual previous executed instruction, originating PC outside the complete candidate, BL/BLX encoding, decoded immediate target or pre-instruction register operand, target ARM mode and expected LR. A stale LR alone is insufficient. An own call, branch or fallthrough cannot become a successful provider boundary. Even a verified external call fails because the adjacent original function bytes are overwritten.

The separately named strict flow is `evidence/application/book_replacement_flow_call_guard_20261030.py`. It rebuilds in its own `work/mechanics-save/20261030-controller-guard` directory and preserves the earlier preferred-flow report and frozen native golden. Its report `book-replacement-flow-call-guard-20261030.json` has SHA-256 `8d6c493167e4d03e95876457ef0a5a86e494082fe569c00a1b56a86c4643e0c8`, identical for normal and unrelated-working-directory replays. Eight profiles complete32 compiled-controller returns and40 native setup returns. None attempts to execute literal data or the overwritten original entry. Saved effects, relevant native calls, provider arguments and all32 ordered frame-write traces still equal the frozen native golden.

The guard controls run actual isolated Unicorn instruction sequences. Outside ARM BL, ARM BLX-register and Thumb BLX-register cases have genuine call edges/LR and are blocked. An outside branch with forged LR, own candidate BL, literal fallthrough and branch to literal interior are also blocked. All seven have zero actual returns and zero provider returns. A separate literal read completes one actual return with the expected word. These are guard controls, not game execution or source coverage. Thumb BLX-immediate decoding is present but has no executed control; unsupported encodings fail closed.

Control report `evidence/application/controller-overlap-guard-controls-20261030.json` has SHA-256 `612954d8788d693e943fec848dc12e0f2080aaefa030d5b03e324679a2325bb3`. Reproduce the controls and strict flow with Python3.13.5/Unicorn2.1.4:

```text
python evidence/application/controller_overlap_guard_controls_20261030.py
python evidence/application/book_replacement_flow_call_guard_20261030.py
```

The unchanged earlier preferred report remains SHA-256 `18541df5ab51f1d4768594fd8b0f157b6fc77bbc0d06e1c2cc0f3b36901e53fd`, and original native golden remains `3b9c1badd9a1beb285b2d0735ab1ab9da6872ec0cc93d400bd31bcfe6f766679`. [The preferred-controller writeup](2026-10-30-preferred-controller-book-replacement-proof.md) states the provider domains and unresolved gameplay paths. This qualification adds zero source bytes and does not make the oversized candidate a valid module replacement.
