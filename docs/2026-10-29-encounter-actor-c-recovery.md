# Actor constructor and transform recovery, 2026-10-29

Two ordinary C bodies now compile and genuinely link to the measured ov000 ARM bytes: constructor `02209DAC`, 556 bytes, and transform `02209D08`, 140 bytes. These 696 bytes remain candidates until the coordinating integrator replays the report and accepts them into a combined module build. This note grants no source credit to their callees, the enemy table, scripts, resource loading, or full scenes.

The accepted-source candidate is `src/encounter/20261029-actors/`, with byte-identical typed hypotheses retained in `nonmatching/encounter/20261029_actor12/`. The header, constructor and transform contain 61, 58 and 23 physical lines respectively, with no code comments or assembly. The initial `20261029_actor11` hypothesis and both profile-search reports remain experimental evidence under the worker's exclusive paths.

## Reproduction and frozen identities

Run the following command from any working directory. The final fresh replay passed from `C:\Users\trevo\Documents\RecProgramming\DQM`, outside the repository.

```text
python C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\nonmatching\encounter\verify_20261029_actors.py
```

| Input or output | SHA-256 |
| --- | --- |
| `src/encounter/20261029-actors/actor_context.h` | `a81006b16716b9caeae8d98787ec41d01bee6a210c9338106999b7d8764d50fe` |
| `src/encounter/20261029-actors/native_ov000_02209dac.c` | `f78c314b23fbe6228ee9a1737bccee4fbeeb9ce3c6727163ea7f76b02328d8db` |
| `src/encounter/20261029-actors/native_ov000_02209d08.c` | `bf6345c333aeaf1cf622b7e329f4bf4798e5d2cb098254ad4486bdee5ec7872a` |
| `nonmatching/encounter/verify_20261029_actors.py` | `239dc356e009154387c25f5ed98dcaef0365c54864c5d8b7715f2882540b51e7` |
| `nonmatching/encounter/actor_fixtures_20261029.py` | `0b679f6bd257f2b89d9fc2f4ecaafbd3cc79de3cffd31ee67a6d5adb0adf8be2` |
| `evidence/matches/encounter-20261029-actors.json` | `8885981bb5951d99c54f1df38cc2412e2dd6e4a3ee795edc6c9325f38d0be459` |

Both entries declare and require the exact header hash before compilation. The report also pins the original ARM9, ov000 and ITCM images and fixture dependencies. Source builds use repository-local MWCC 2.0 SP1p5, SHA-256 `89b2fc16c7f1f29ede1e52bdee5bc8ae4d63fe7e50d8074354dfd92c43d47aca`, with ARM946E and inline off. The constructor uses O3 and the transform O2. Each freshly built body passes the real MWLD link and complete byte comparison; callee anchors contribute zero source bytes. These profiles are local evidence for these units and do not establish a project-wide configuration.

## Independent execution evidence

The fresh original-versus-linked-C replay passes 1,703 actual returning calls per implementation, 3,406 total, using 1,419 separately initialized machines per implementation. It compares R0 through R12, SP, LR, PC and CPSR; ordered CPU store addresses, sizes and values; persistent and VM state; and the complete actor pool, actor-global block, metadata manager/cache and mapped table snapshots after every actual return. All counted calls must reach the return sentinel and preserve SP and R4 through R11. Original callees execute without native-function stubs.

New fixtures include 72 successful direct constructor cases with nine real native IDs, eight raw mode values, first-free slots 0, 1, 17 and 47, byte selector aliasing, position and angle words, and four byte field values. An independently assembled expected record checks all 708 actor bytes, including the zeroed fields, fixed-point squared scalar, initial state, metadata-derived fields, sentinels and conditional transform results. All nonselected actor records and persistent save bytes remain unchanged. The tested native IDs are 0, 21, 42, 117, 770, 771, 1398, 1399 and 1420.

Native ID 42 with mode 0, slot 0, selector/group 7, field byte 0, XYZ `[-12288, 0, 8192]` and angle `-32768` actually returns after **36,707 instructions**. Across the 72 direct cases, observed counts range from 32,533 to 41,493. The explicit constructor limit is **100,000 instructions**, with a one-second execution timeout; the default for other direct routines remains 20,000. A local oracle subclass supplies this limit, leaving the earlier frozen 20,000-instruction fixtures unchanged.

Twenty direct transform fixtures preserve every actor byte outside the measured output vector at `+0x284..+0x28F`. Four zero-angle cases independently check `[0,0,length]`; nonzero-angle cases compare native and rebuilt execution without claiming an independent trigonometric model. Existing selector getter/setter and full-pool/mismatched-selector SYS10 fixtures also rerun. Returning outer calls reach the reconstructed constructor 120 times and transform 36 times per implementation.

Four additional positive SYS10 wrapper probes, one per VM thread, reach the constructor's common return instruction but subsequently fault at ov000 ARM `02210CE8` because the wider resource context is absent. They are recorded as unsupported boundaries, excluded from the 1,703 returning calls, and supply no post-fault state proof. The entire SYS10 wrapper and a playable scene are therefore uncertified.

## Original metadata and manual manager context

The fixture uses the original ROM file `FldEnmyPrm2.bin`, 62,532 bytes, SHA-256 `61866ed8e213a561ab6f262b0dccf4cdceba4f4b0e4620a3e5a77eae58c0366b`. It independently checks the extracted file against the file allocation interval in the pinned 175,959,612-byte input ROM. The file consists of an eight-byte FEPT header followed by 1,421 records of 44 bytes. All 1,421 records have native-ID, exact file offset and record-hash entries in the report; this static provenance does not imply execution coverage for every record.

The main ARM metadata getter is `020C56B4`. The native loader at `020C55DC` stores its handle at manager `021D5404` and the record base at manager `+4`; the latter points eight bytes into the file. The fixture maps the unchanged file at synthetic RAM `026C0000`, writes `manager+4=026C0008`, uses a zero handle, and initializes the 24 cache IDs at `021D540C` to -1 with their record payloads zeroed. Each cache slot occupies 48 bytes. This is explicitly manual data-context setup: the file loader, allocator and real file handles are not exercised, and no provider function is stubbed.

Eleven valid native getter calls independently return the exact corresponding ROM-backed 44-byte slices for IDs 0, 1, 21, 41, 42, 117, 770, 771, 1398, 1399 and 1420. The original loader separately contains a hardcoded compact-lookup initialization bound of **1,399**, loaded from main ARM literal `020C5674`; its compact lookup is at `021D588C`. The verifier pins the full original module and checks the bound, manager and lookup literals and filename. The loader's 156-byte range SHA-256 is `c9fc2fa2a81579c3f22d0fb6d9891840118a27493ce436056e39b68680bdb1f3`.

The measured 1,399 initialization bound and the modified file's 1,421 record count remain separate facts. Neither is repaired. Direct success for IDs 1399 and 1420 proves neither compact-lookup initialization nor model, renderer, asset or gameplay compatibility for those entries.

## Source choices, failed experiments and limits

The first constructor hypothesis had the correct 556-byte size but only 504 matching bytes in its best profile. Ordinary C changes recovered the remaining instructions: preserve the shared return through nested success guards, give the stack field its measured byte width, and retain the original `~0xF0` mask. The transform already matched from the initial typed hypothesis. No instruction bytes, executable arrays, assembly or artificial register annotations were introduced. The earlier profile driver's `compiledProfiles` counter has a known object-name lookup defect; actual compiler entries and genuine linker proofs determine success.

The header uses measured 32-bit target layouts, including the 708-byte actor and 44-byte enemy record. Field names identify measured offsets except where arithmetic behavior is explicit. The constructor's repeated binary32 conversions use explicit native `_fflt`, `_ffix`, `_fadd` and `_fsub` ABI bindings, followed by a signed 64-bit multiply and fixed-point shift. Those helpers receive no new source credit. The evidence covers the selected finite table values, without extending C conversion or overflow guarantees to malformed inputs or a native Android port.

Negative IDs, IDs at or beyond 1,421, malformed file headers/lengths, invalid manager pointers and allocator/resource failure behavior remain untested. Mapped zero bytes beyond the real table are not enemy records. A returned fixed-pool actor index does not establish that a script is reachable, an enemy can appear in the current scene, a story/quest predicate is satisfied, or an encounter is repeatable. Interpreted script logic remains a separate reconstruction backlog. Whole-module acceptance and whole-ROM source reconstruction remain the integrator's separate gates.
