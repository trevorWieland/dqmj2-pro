# ARM7 rate and parameter source packet

The measured private host ARM7 main image supports four complete ordinary C functions totaling 400 initialized bytes: 368 instruction bytes and 32 generated literal bytes. This packet is function matching evidence pending the integrator's complete module and ROM gates. It adds no executable inventory extent, source data, assembly, callee, constructor, or complete-game credit.

| ARM entry | C definition | Complete bytes | Paired vectors | Actual owned returns |
| --- | --- | ---: | ---: | ---: |
| 027EA4D0 | WElement2RateSet | 180 | 2,072 | 4,144 |
| 027E9578 | WSetBssid | 100 | 192 | 384 |
| 027E9744 | WSetDTIMPeriod | 68 | 20 | 40 |
| 027EAD78 | RND_init | 52 | 112 | 224 |

Both reports are rebuilt by `python validate_arm7_sdk252_rates_parameters400_20261101.py`. No cached objects are inputs. The validator starts each pinned matcher, which compiles authored C, splits unchanged relocations, genuinely links with the pinned MW linker, compares every byte, and executes original and freshly linked C bytes independently in fresh Unicorn states. All 11,136 observed nested reader/copy returns are separate from the 4,792 owned returns. The parameter prerequisite also observes 648 native clear returns at the actual prefix return PC/SP; its enclosing constructor is stopped at a boundary and receives zero normal-return credit.

The 174 negative controls comprise 72 metadata/product controls, 70 direct caller-policy controls, and 32 native prerequisite controls. Eight separately compiled wrong-C hypotheses produce 4,792 actual returns and 3,602 independent-model rejections. Two additional invalid-period pairs produce four actual returns with a null runtime pointer because native argument rejection precedes the pointer load. Those four diagnostic returns are reported separately from the main corpus. The initial negative test incorrectly required this invalid-period path to fault; the corrected control selects a valid period when testing the pointer prerequisite.

The unrelated-CWD cold proof preserved both populated WORK directories, verified that their original paths were absent, and invoked the complete validator from the existing Codex workspace. Every source and canonical match report hash remained identical. Its receipt is `evidence/verification/arm7-sdk253-rates-parameters400-cold-20261101.json`; WORK archives and compiler/native outputs are regenerated products and are not transported as source inputs.

## Source and layout

The typed ordinary C derives from the pinned public ntrtwl/NitroSDK revision `ccbbcc8b6db4c4dbba3d503d2026978d78977840`, specifically the WlNic source and its closed SDK type hierarchy. This is comparative reconstructed SDK source, not proof of the game's SDK revision or historical authorship. Its licensing follows that repository; no CC0 attribution is inferred. The prior reference manifest independently records original lengths, Git blob identities, and SHA-256 values. Final compiler inputs are comment-free local C/includes, with no provisional parse headers, system headers, assembly, or opcode transcripts.

The parameter C and four include fragments preserve the closed named-word SDK group. Only the three tabled parameter definitions receive candidate credit; its other C definitions do not. The rate conversion is a separate standalone typed C definition. Compiler layout proves a 0x694-byte WL_MAN view, Rand.a at 0x5F0, Rand.b at 0x5F2, Work.BSSID at 0x3A8, and Work.DTIMPeriod at 0x3B8. MW long, pointer, and relevant target words are four bytes. Native instructions independently agree on each field address and store width.

The rate table at 027F73C0 contains 120 halfword entries, totaling 240 initialized bytes. An initial 108-entry declaration matched 179 of 180 function bytes and emitted the wrong bound at 027EA518. The complete 120-entry view matches every byte and is independently checked against the twelve-rate mapping with invalid sentinels. This is a declaration/boundary correction; the original table remains an original data dependency with zero reconstructed-data credit. The failed extent is retained in `evidence/attempts/arm7-sdk249-rate-table-extent-correction-20261101.json`.

## Measured behavior and limits

The rate function initializes two halfword masks and consumes a length byte plus each rate byte through original WL_ReadByte at 027EAD5C. The low seven bits select a supported rate or the 0x8000 invalid marker; the high bit additionally selects the basic mask. Declared SUP_RATE_ELEMENT capacity is two bytes. Source-compatible fixtures therefore restrict length to 0..2, use readable complete four-byte structures, and keep the four-byte output nonoverlapping and halfword-aligned. Every raw rate byte is exercised across two alignments; the two-rate corpus is deterministic rather than an exhaustive enumeration of all possible pairs. Longer arrays need a separately qualified C view and receive no portability claim here.

The BSSID function retains both real WSetMacAdrs1 calls at 027EA0EC, copying three halfwords to context+0x3A8 and MMIO 04808020, then clearing bit10 of 048080D0 when source halfword bit0 is set or setting it otherwise. Fixtures vary raw words, control values, source alignments, and context alignment. The parameter source pointer must reference six readable bytes and remain separate from destination storage.

The period function returns 5 with no non-stack stores outside 1..255. Supported values store a halfword to context+0x3B8 and 0480808E, clear 04808088, and return zero. Its public source argument is u16; the fixture rejects a synthetic 65536 producer rather than claiming that value is source-compatible. Zero and 65535 also independently return 5 before the runtime pointer is used.

RND_init takes two full u32 words. It stores `((a & 0xFFF8) + 5)` narrowed to u16 and `(b | 1)` narrowed to u16. It is declared void; incidental native R0 is compared physically without assigning return meaning. Fixed edge vectors cover full-word high bits and narrowing; they do not exhaust the 64-bit input Cartesian product.

All routines compare CPU registers, flags, stack, complete mapped memory, ordered stores, termination mode, and actual helper returns. The independent models verify complete non-stack memory and expected writes. MMIO is a deterministic mapped snapshot. No physical wireless hardware, concurrent updates, interrupt delivery, network validity, caller scene reachability, or game progression meaning is proved.

## Narrow runtime pointer policy

The original descriptor prefix installs the absolute word at 0380FFF4 from incoming descriptor word0. It is not classified as this module's BSS or reconstructed data. The new parameter adapter admits only the exact three qualified ARM identities, current profile/source/include/module hashes, and the existing producer witness. It preserves every other function/data guard, restores the base binding function on success/error, and retains default refusals and neighboring-word controls. Rate conversion uses the unchanged base linker without any exception.

The normalized accepted-cohort129 export is checked with integer address normalization across processor/program/module/mode. All four ranges are absent there and are kept separate from pending earlier source packets. Whole-module adoption and future shared inventory updates remain the integrator's responsibility.
