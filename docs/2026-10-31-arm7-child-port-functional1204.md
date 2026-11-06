# Four complete child ARM7 port-transfer hypotheses

Four full ordinary-C hypotheses now compile and genuinely link through MWLD, and agree with original execution in 408 bounded synthetic contexts: 816 actual original/C returns. The qualified program is `dwc/utility.bin/move/child.srl`; all four entries are ARM code in `utility-child-arm7-main`. They remain zero-credit nonmatching source, with no module or whole-ROM adoption.

| Native entry | Native bytes | Linked C bytes | Cases | Actual original/C returns |
| --- | ---: | ---: | ---: | ---: |
| 027F6428 | 300 | 288 | 104 | 208 |
| 027F6554 | 300 | 288 | 104 | 208 |
| 027F6680 | 316 | 308 | 100 | 200 |
| 027F67BC | 288 | 280 | 100 | 200 |

The input image SHA-256 is `a5838c09ff9e04d2ffbdf780b3d1bbd5b5875dda9f2ea7d7f8eed74a60d1920a`, tied to the measured ROM. Every C body is linked at a separate virtual address `026A0000`; it cannot fall through to original code or delegate to an original helper. Original instructions, object instructions and relocation addends are not patched. Only the two measured halfword port addresses, `040001C0` and `040001C2`, are accepted external bindings. The real linker checks each virtual symbol's address and complete emitted extent.

The boundary supplies finite synthetic bit-`80` control polls and independent 16-bit received values. It records ordered port and destination writes, port reads, source-buffer byte reads, complete buffer and guard hashes, final port words, raw R0, callee-saved registers, SP/LR and return mode. Each original or C execution starts in a fresh Unicorn machine. No physical bus, peripheral, storage medium, firmware or caller scene is executed.

The two emitters send raw opcodes `02` and `0A`; the two capture routines send `03` and `0B`. The latter has one extra dummy transfer. These are measured raw output sequences. The current fixture does not infer a device command's meaning or grant a physical I/O result.

The repaired source addresses two independent M2C type problems. The initial address was inferred as a byte, hiding real upper address bytes and allowing generated code to omit explicit low-byte operations. Widening that parameter to a full word requires restoring native `ANDHI R1,R0,#255` before the emitter count remainder and the low-byte mask before writing the third command halfword. Merely changing its declaration gives a wrong remainder: address `1234F0`, requested count 32 produces `CC10` in the old typed draft instead of the native 16. Both old writer hypotheses are preserved, genuinely recompiled and demonstrated not to complete the supported 16-byte model context within its bounded execution.

The three command halfwords are an actual contiguous `u16 command[3]`. The former generated code indexed across separate local variables, which is not a defined C array. Byte pointers now express actual buffer loads/stores, and only the measured halfword ports are volatile. No volatility is added to ordinary RAM to influence matching.

Zero-count entry returns the incoming address word without port activity. Positive captures return the final zero-based output index; positive emitters return the clear masked control value, zero. These are observed raw R0 contracts, not success or device-validity classifications. Address high bytes, low-byte boundaries, zero/one/multiple transfers and both clear/delayed polling paths are exercised.

The native count guard uses unsigned 32-bit wrapped addition followed by a page-number comparison. It is not an unconditional transfer-boundary rule. For example, at raw address `FFFFFFFF`, count 2 wraps the last-address expression and bypasses the ordinary clamp. Separately, emitters use a signed comparison against `count-1`; the synthetic `80000001` and `FFFFFFFF` count cases can therefore take the final-byte path immediately when the preceding unsigned guard does not clamp. These measured paths are retained without asserting that real callers or devices accept those values.

The code deliberately leaves several claims open. Caller-scratch R1/R2/R3/R12, final APSR flags, internal temporary-stack layout and instruction offsets differ or remain unmatched; they are recorded in the traces and excluded from functional equivalence. All positive scenarios have an internal-state difference, which includes their different instruction-offset sets and stack layout. This does not mean every scratch register differs in every scenario. A permanently set control mask and one-instruction budget stop without a return and receive zero return or supported-error credit.

The complete per-case traces use deterministic gzip with `mtime=0`. The report declares compressed and raw hashes, lengths and reproduction paths. Builds regenerate every source object, ELF, binary and trace before writing the report; none is an input cache. The canonical report repeats byte-identically from an unrelated working directory:

`fe869a975798f8d9320b4530a8d377cc3ec4fd88d8ddbcf1c9ca64fb16f35162`.

Eight bounded compiler profiles per function were tried after the functional proof: MWCC 1.2/sp2p3 O1/O2 with space/speed, 2.0/base O2 space/speed, 2.0/sp1p5 O2 space and 2.0/sp1p6 O4 speed. None gives exact bytes. Two additional context probes per function express the same measured hardware ports as ordinary constant volatile pointers; these also compile without an exact match and have no new functional or source credit. The 308/288/280/288-byte ordinary-C drafts remain the functional baseline; compiler-only tuning rotates to another queue rather than forcing assembly or artificial register constraints.

## Reproduction

```powershell
& C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe C:\Users\trevo\Documents\RecProgramming\DQM\j2p-recovery-lanes\arm7\prove_arm7_spi_functional1204_20261031.py
```

Sources and profile are in `nonmatching/arm7-bulk/20261031/lane-spi-functional1204-v1`; the old typed sources remain separate. This work adds four functional hypotheses and no accepted decompilation percentage.
