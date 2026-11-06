# Native SYS dispatcher C recovery — 2026-10-29

ARM9/main/ARM/0205A65C now has a matching ordinary-C reconstruction of all 5,792 native bytes. A fresh pinned compiler build, genuine MWLD link and paired original/rebuilt execution pass. Source and its complete include closure are promoted to `src/encounter/20261029-sys-dispatch/`; byte-identical original typed hypotheses remain in `nonmatching/encounter/20261029_sys09/`. Registration and the combined module build remain coordinator-owned.

Run `python nonmatching/encounter/verify_20261029_sys_dispatch.py`, optionally adding `--source-root src/encounter/20261029-sys-dispatch`. The source root resolves against the repository rather than the caller's CWD. The final full replay passed through absolute invocation from the parent DQM directory. Results are in `evidence/matches/encounter-20261029-sys-dispatch.json`.

The C switch reads the current thread's PC and native SYS opcode. Its table spans 0 through 357, with 355 recognized opcode labels, 353 native case blocks and 349 distinct qualified handlers. Opcodes 0, 275 and 278 select the default zero-return block, as do values outside the table. Other calls return the dispatch success value one. Sixteen blocks forward an explicit third mode word, zero or one, matching the original R2 setup; no bank or gameplay meaning is assigned to that modifier. All other calls forward VM and instruction pointers. Handler return values are not substituted for dispatcher success.

This is native interpreter control flow, not recovered SCR application logic. The switch is ordinary C with named handler calls and explicit argument widths. The four included case fragments keep every authored file below 500 formatted physical lines: the main source is 370 lines, with fragments of 301, 301, 300 and 159 lines. They are C statements compiled into the original dispatch, not generated instruction bytes or script transcriptions.

The compiler is the verified private `2.0/sp1p5/mwccarm.exe`, SHA-256 `89b2fc16c7f1f29ede1e52bdee5bc8ae4d63fe7e50d8074354dfd92c43d47aca`, using its separately demonstrated O4/ARM946E/soft-float/inline-off profile. The independently pinned linker SHA-256 remains `bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74`. Full flags, source/object hashes and link artifacts are recorded per entry. Main C SHA-256 is `a88d48ffce4907308ccfa3f84efeaf0a08b34540baedee46c200b58a7e867fef`.

| Required source dependency | SHA-256 |
| --- | --- |
| sys_cases_0.inc | aaff011d575126ce8b3ef66100409c8c8882ce3b0d1cb512eeebe9270c82e071 |
| sys_cases_1.inc | fc41cdcb4db73cffa10b8ab072246ee7f1f100d3ad8dc8ab8601b3a0e467c993 |
| sys_cases_2.inc | 6fe39a7ec0e280b53552c95c868fddefce80d85aa95b2c33497831729ed36c4e |
| sys_cases_3.inc | 9284884f4bdfbe34f6d9cef6883df71605fe3d399519a54c86ed57bf7deb6f0b |
| vm_context.h | 6b0a4de328e3dd4289ffd0aaaa30f67e7faf3efe268287aad64df7db5f58b3f8 |

Every dependency above is checked before compiling and declared in the entry's source closure. There is no assembly or instruction patch. All 349 handler anchors initialize zero executable bytes and receive zero extra source credit. Their processor/module/address/mode bindings come from measured native identities; the remaining handler bodies remain independently tracked work.

## Windows linker argument handling

The original absolute-object sweep produced exact compiler candidates but could not launch the linker: Windows returned `FileNotFoundError: [WinError 206] The filename or extension is too long`. Those failed attempts are preserved without source credit in `evidence/attempts/encounter-20261029-sys-dispatch-long-argv.json`. The earlier apparent byte equality after declared relocation is not counted as a successful actual link.

The fresh verifier performs a process-local argument transformation only for the independently pinned real linker. It converts file paths within the explicit link CWD to relative arguments. The executed command has 4,639 characters, compared with 53,919 characters for the unshortened command constructed for that fresh directory. The same files, input hashes, argument order and non-path options are checked before execution; the proof records the actual executed argv and CWD. The executable and existing license configuration remain repository-local pinned tool dependencies.

Input/output paths are resolved before shortening and must remain within that explicit link directory. Three negative cases reject relative traversal and absolute escapes before linker execution. The temporary subprocess wrapper is restored afterward. No shared framework file is edited, no instruction or relocation is changed, and no fake linker is substituted. The unchanged real MWLD emits the exact original caller span. This resolves command transport for the large source unit rather than changing code-generation or matching rules.

## Fresh execution and limits

The final paired run passes 6,812 actual returns per implementation, 13,624 total, with 2,655 independently initialized machines per implementation. It preserves all preceding context/thread/operator/builtin/SCR-prefix controls and adds 128 direct SYS-default cases across four thread slots and four code offsets. The dispatcher is reached 1,189 times per implementation. Original and freshly linked replacements compare all R0–R12/SP/LR/PC/CPSR, ordered CPU store addresses/sizes/values, the full 0x7040-byte persistent partition and both 0x8A0-byte VM contexts. Every counted call truly reaches the return sentinel, restores SP and callee-saved registers, stays below 20,000 instructions and uses the one-second bound.

All comparisons pass. The known SYS5/SYS104 and null-resource-load probes remain nonreturning, excluded and unsupported; no post-fault state is proof. No native function is stubbed. The complete 5,792-byte comparison covers all caller instructions and table layout, while the bounded fixtures exercise the supported contexts available so far. They do not certify every one of the 349 handler bodies, every game scene or every malformed input.

The previous APSR comparison, two-register signed division, raw-bit cell and Android-domain limitations remain explicit in the preserved regression data. Pointer-bearing VM structs still model ARM32 rather than Android64. Unsupported opcodes returning zero from this dispatcher does not prove they safely finish as complete VM threads.

The separate interpreted backlog remains 297 unique SCR images with zero recovered ordinary script source. Neither this larger native caller nor its opcode table contributes script-source credit. This is not a complete source module, whole-ROM source match, native Android run or encounter-access/renewability certificate.
