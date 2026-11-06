# ITCM reset clear, 2026-10-29

The measured ARM9 ITCM span `0x01FF82B4–0x01FF82C8` is the five-instruction `OSi_CpuClear32` original assembly definition in the preserved SDK source. The new symbolic assembly source matches all 20 native bytes after fresh assembly, without embedded byte arrays or external callee bodies. This contributes 20 justified original-assembly bytes and zero ordinary C bytes.

## Provenance

The pinned third-party preservation source is [NitroSDK os_reset.c](https://github.com/ntrtwl/NitroSDK/blob/1958e1ef5547b076c793047b0fc0e39e79b416c7/libraries/os/src/os_reset.c), commit `1958e1ef5547b076c793047b0fc0e39e79b416c7`. Its 9,242 bytes hash to SHA-256 `ee5654e4074a671318ede7d32ae1d5024e1261f4d1de5ba8f662d70386085b3a`; the independently calculated Git blob hash `67874d20df3d27aa02eb09f4788c7a4db3d7560b` agrees with the credential-free contents API response. Acquisition files remain in `work/lowlevel-recovery/20261029-itcm/sdk-reset-reference/`.

This is third-party preservation evidence, without a separately authenticated Nintendo source archive or vendor signature. The native byte match independently establishes that the five instructions are present in this measured executable. The conditional SDK workaround branch is absent from these native instructions. The following 168-byte `OSi_ReloadRomData` definition is ordinary C and receives no assembly credit.

The permanent provenance record is `evidence/itcm/2026-10-29-reset-clear-provenance.json`. The verifier pins that record and the local assembler hash before building.

## Reproduction and checks

Run `python verify_itcm_20261029_reset_clear.py` from the repository, or invoke that script by absolute path from another working directory. The report is `evidence/matches/itcm-20261029-reset-clear.json`.

The verifier removes its previous compiler output, assembles the symbolic source with the pinned MW assembler, rejects unresolved relocations, and compares all 20 native bytes. It additionally runs `mwldarm` through `link_runtime_unit.validate` and compares the actual linked caller span. This isolated source-only link contributes no callee, module, or whole-ROM completion claim.

Fresh native and source Unicorn instances run 222 paired fixtures, comprising 220 valid return cases and two explicitly separate unmapped-write fault cases. Their 444 total executions include 440 actual returns and four faults. Both ARM and Thumb return modes are covered. All five native instructions are visited. The independent model checks the complete 4 KiB RAM arena, ordered word writes, R0–R14, and final subtraction NZCV flags, including signed end-address boundaries, zero counts, and partial word counts. The word-aligned RAM fixtures do not establish unaligned STM behavior, physical bus-abort behavior, or complete reset/hardware timing.

## Remaining ordinary C experiments

No partial ordinary C experiment is accepted by this report. The `0x01FFA988` draft improves to 514/520 matching bytes after correcting reset store order; its initial two instruction order remains wrong. `0x01FFF068` remains 501/508, and `0x01FFC890` remains 1,263/1,268, with register allocation differences. Bounded `-sym off`, `-sym full`, and `-sym on` profiles do not close these mismatches. The 168-byte loader has an ordinary C 140/168 draft after correcting pointer arithmetic and source-word lifetime. Matching C recovery continues separately.

These source files, the report, and the isolated linker output require integrator adoption before shared ledgers or accepted module builds count this span.
