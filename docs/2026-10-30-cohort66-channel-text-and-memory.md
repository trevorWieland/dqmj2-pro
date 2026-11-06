# Cohort 66 channel, text and memory source — 2026-10-30

The accepted build measures 8,759 native functions and 615,621 initialized source bytes, or 24.5010% of the current 2,512,636-byte inventory. Nine new functions contribute 1,784 bytes. Another 1,897,015 inventoried bytes remain unresolved. This percentage includes source-generated literals and alignment and is not overall game completion. Executable discovery and complete game behavior remain separate requirements.

| Module and entry | Bytes | New ordinary C evidence |
|---|---:|---|
| ARM7 WRAM `037FF3AC` | 948 | Channel state update; 1,630 caller returns and 35 controls |
| ARM9 main `0206CE54` | 240 | Sprite release; 2,808 caller returns with actual registry removal |
| ARM9 main `0201B018`, `0201B080`, `0201B124` | 176 | Default locale dispatch and wide-to-byte loop; 1,854 caller returns and three controls |
| ARM9 main `0201B21C`, `0201B248`, `0201B288` | 284 | Byte search, comparison and fill; 4,928 caller returns and four controls |
| ARM9 main `0201B09C` | 136 | Byte-to-wide caller; 2,566 caller returns and three controls |

The ARM7 corpus distinguishes 452 caller returns without BIOS services from 1,178 using synthetic SVC table contracts. No original BIOS execution is claimed. Sprite release executes actual native unregister logic but provides heap-free service returns; deallocation and ownership are not inferred. The text routines establish default locale byte widening/truncation, not save-label or Japanese text encoding. All 40,560 semantically unknown save bytes remain unknown.

Run `python validate_cohort.py --cohort 66` for the shared acceptance build. Both checksum byte matches, 36 vectors / 144 isolated returning executions, 5,117 getter comparisons, all 20 initialized module comparisons, all 20 actual preferred source selections, current negative/freshness checks and source policy pass. The constructed ROM is exactly 175,959,612 bytes with SHA-256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`. It retains original executable scaffolding. Source-only ROM reconstruction and a Windows game built from source remain false.

The strict application audit continues to detect concurrent outside edits. Baseline and ROM/save input hashes are unchanged; no snapshot was replaced. Independent clean checkout S is replaying repaired cohort 64, and T is replaying immutable cohort 65 with the historical-output guard. Neither ongoing run is claimed as a completed clean regression of cohort 66. The last completed clean suite remains checkout P at cohort 53 plus deadline tooling.

A new worker validator briefly wrote its 492-byte flush controls to the earlier 948-byte channel control-report path. The misplaced artifact and collision receipt are preserved. The unchanged 948 validator actually reran all 35 controls and restored exact report hash `6fc6168305e3838dfa681b2243a3869a2d87aca72c88f8cb2dfe7fd7e6f2d8b5`. Frozen source/header/matcher inputs were unchanged. The central cohort evidence audit completed after restoration. The newer flush function remains outside this cohort.

The same three memory sources also compile for Windows x64 and Android AArch64. Windows passes 2,464 actual C-interface calls against native golden results and full-buffer snapshots. A standalone Android runner with the same synthetic vectors is compiled and packaged privately; Android execution count remains zero. See `docs/2026-10-30-memory-primitives-native-port-validation.md`. No game assets or saves enter that bundle, and no device or dual-screen test is implied.

Source and evidence details are in `docs/2026-10-30-native-byte-text-and-memory-source.md`, `docs/2026-10-30-arm7-channel-update-source.md` and the dated sprite-release writeup. The machine acceptance record is `evidence/verification/cohort-2026-10-29-66.json`; the committed closure audit is produced after the source commit. Later candidates receive no credit here.

The committed source closure audit at `62329bcc` checks 8,523 repository paths and 112 explicit copied dependency paths with zero missing paths or hash mismatches. See `evidence/verification/cohort66-committed-source-closure-20261030.json`.
