# ARM7 channel-start field initializer source — 2026-10-30

Host ARM7 WRAM ARM 037FFEB8 rebuilds as complete ordinary C and matches all 56 initialized bytes through real pinned Metrowerks linking: 52 instruction bytes plus one 4-byte generated constant. The literal FFFE9680 is signed -92544 data stored at destination+0x10. It is not an executable address. The routine also writes byte+2=0, full incoming word length at+0x34, halfwords+0x30/+0x2E=0 and the original flag byte at+3 OR 3. Other bits and bytes remain unchanged. The view describes only these accessed fields; it does not reconstruct the complete channel allocation or imply an object size of 56 bytes.

The independent corpus uses 305 fresh synthetic contexts, including all 256 initial flag bytes, six selected full 32-bit input words, aligned/page-crossing views and one persistent two-call context. It records 612 actual original/recompiled entry returns with six ordered stores per invocation. Both code versions agree with an independent complete mapped-memory and register model. That model predicts all general registers and preserved CPSR, including incidental scratch values; all RAM/BSS/stack and ordered non-stack writes match. The API remains void, so preserved R0 is not assigned a logical return meaning.

No lower helper/provider executes. The direct native range contains 52 ARM code bytes and the single 4-byte literal pool; all own instructions are visited. Single-instruction exhaustion and an unmapped destination have zero return or supported error-result credit. These are disposable data-only contexts: no physical audio, caller legality, ownership, complete channel reset or gameplay meaning is proved.

The standalone comment-free source is src/arm7/20261030_channel_start/native_arm7_wram_037ffeb8.c. Its typed partial view is independently byte/link/native validated. Reference-only naming/structure support is the byte/Git-verified pokediamond SND_exChannel.c at commit b623abef1b4dfe204ca50aab42447ac00c134290, ExChannelStart. The same SDK version and unique original compiler flags are not presumed. No executable assembly, byte arrays, patched instructions, original object body or changed relocation addends are compiler input. There are no external relocations; the required measured nativeSymbols/nativeSymbolEntries publications are correctly empty.

The validator freshly reconstructs the source and native proof, checks product/input availability even after caching and passes 31 rejection controls. Four in-memory variants alter the zero initializer, omit the full-word length store, change the start/active mask or corrupt the attenuation literal; the independent effects/register model rejects them. The actual wrong-C literal variant is compiled and truly linked, correctly failing exact comparison. Accepted compiler products are then restored. All prior frozen batches remain unchanged, and no shared registry is edited by this worker.

Reproduce using the pinned absolute interpreter from any directory:

```
C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\match_arm7_channel_start_20261030.py
C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\validate_arm7_channel_start_20261030.py
```

The matcher directly regenerates evidence/matches/arm7-channel-start-20261030.json; controls are evidence/verification/arm7-channel-start-controls-20261030.json. This unit has zero original-data, helper, module and ROM credit, and complete module acceptance remains a coordinator gate.
