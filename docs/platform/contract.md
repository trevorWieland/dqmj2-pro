# Platform contract — hardware/SDK boundary of the matched ARM9 code

Status: evidence report plus a declaration-only interface header (`include/platform.h`). No build
target is added. Everything below is derived from matched source in this checkout; each item cites
the file and function. Items without a matched reader are marked **UNKNOWN** and are not invented.

## 0. Method and evidence limits

* `config/arm9/symbols.txt` has 8,919 lines but only 35 carry SDK names; the rest are
  `func_<addr>`/`data_<addr>`. The named ones are the low region of the main image:
  `HuffUnCompReadByCallback` `0x02000088`, `GetCRC16` `0x020000f6`, `Sqrt` `0x02000156`,
  `RLUnCompReadNormalWrite8bit` `0x020001b8`, `Halt` `0x02000246`, `IntrWait` `0x020002ae`,
  `Div` `0x0200030a`, `BitUnPack` `0x02000360`, `VBlankIntrWait` `0x020003e6`,
  `LZ77UnCompReadNormalWrite8bit` `0x0200043e`, `SoftReset` `0x02000496`, `WaitByLoop`
  `0x020004fc`, `CpuSet` `0x0200064a`, `CpuFastSet` `0x020007a6`, `Mod` `0x0200073c`,
  `IsDebugger` `0x020005ea`, `Entry` `0x02000800`, then `main` `0x02000c34`. Those are matched as
  assembly under `src/hardware/bootstrap_bios/` (e.g. `native_main_bios_020002ae.s` = `IntrWait`).
* Matched C in `src/` calls the rest of the SDK through `native_fn_<addr>` symbols, so the SDK
  service name is often not recoverable. Where the ABI shape is clear from the matched caller but
  the callee's identity is not, the contract marks it **INFERRED**.
* No matched main-module reader was found for the NitroFS file API, input, or the ARM7 boot
  handshake. Sound has exactly one proven ARM9 wrapper (see the catalogue); the rest of the sound
  service is unknown.

## 1. Service catalogue

| service | matched evidence (file → function) | ABI shape | hardware/SDK assumption a port must satisfy | confidence |
| --- | --- | --- | --- | --- |
| IRQ save/restore | `src/hardware/main/native_main_hw_02007ff4.s` and `native_main_hw_02008008.s` (matched asm): `mrs cpsr` + set I bit `0x80` to disable; restore ORs the saved I bit back | `u32 (*)(void)` returns the previous CPSR I bit masked to `0x80`; `void (*)(u32)` restores it | A port must provide a critical-section primitive equivalent to the ARM CPSR I bit; this is **not** an IME register write | proven-by-code |
| VBlank/IRQ wait | `src/hardware/bootstrap_bios/native_main_bios_020002ae.s` (`IntrWait`), `020003e6.s` (`VBlankIntrWait`) | `(u32 discard, u32 mask)` / `(u32 discard, u32 state)` | Vertical-blank IRQ must be deliverable; a headless port needs a virtual clock or VBlank pump | proven-by-code (symbol name + matched asm) |
| Boot register sequence | `nonmatching/main/20261029-broad01/native_main_02026b28.c` (draft source, nonmatching, zero credit; ledger `0x2026b28` `functionMatched: false`); the same sequence is visible in the disassembly | `void (*)(void)` | Write order: IME=1, POWCNT1 `0x04000304` = `(old & 0xfffffdf1) | 0x20e`, DISPCNT `0x04000050`=0, four DISPSTAT `0x04000060` RMWs, `0x04000580`=0xbfff0000, then subsystem inits | draft-derived, not matched |
| Display control | `src/runtime/runtime03/native_main_02041774.c` calls `native_fn_020042e0(0x04000050, mode, flag)` and `(0x04001050, …)` for engine B | `(u32 register, u32 mode, u32 flag)` | A DISPCNT-like register at `0x04000050` and engine-B at `0x04001050`; setter name `native_fn_020042e0` is UNKNOWN | ABI proven, setter identity INFERRED |
| DMA | `src/itcm/dma.c` (`native_itcm_01ff8448`, `-8488`, `-84f8`, `-851c`) | `(s32 channel, u32 src, u32 dst, u32 control)` | Registers `0x040000b0 + channel*12` = SAD/DAD/CNT; channel 0 reads SAD twice as a write barrier; control `0x81400001` for immediate copy | proven-by-code |
| CPU copy/fill | matched callers of `CpuSet` `0x0200064a` and `CpuFastSet` `0x020007a6` (named SDK symbols) | `(const void *src, void *dst, u32 control)` | Fill vs copy selected by argument bit; word/halfword unit selected by control | proven-by-code (bit semantics INFERRED) |
| Heap/alloc | `src/ov006/p1k_ov006_thumb/native_main_021f1f0c.c` allocates through vtable `0x0221aad0 + 0x04` and zero-fills; `src/main_sdk_aux/20261101_frame_heap_core324`, `20261101_heap_search356`, `20261101_heap_attribute424` | `void *(*)(u32 bytes)`; 0 on failure; block headers 0x18 bytes seen in heap sources | A two-level heap (arena, attribute, search) with the same failure contract; host malloc is acceptable if sizes/headers are preserved | alloc contract proven; free path INFERRED |
| ARM7 IPC FIFO | `src/runtime/20261101_fifo_send136/native_main_0200a440.c` | `s32 (*)(u32 channel, u32 payload, u32 flag)`; 0 ok, -1 full, -2 send-empty | Word layout `channel:5, flag:1, payload:26`; status `0x04000184` bit14 full/bit1 empty; data `0x04000188` | proven-by-code |
| Card command bus | `src/mechanics_save/20261029_card_command.c` | `(u32 first, u32 second)`; control `0xc0`, 8 command bytes at `0x040001a1`; poll `0x040001a4` bit31 | Raw card bus, not the NitroFS read API | proven-by-code |
| NitroFS/file read API | none matched in main source; host side only (`ports/native-storage`, `ports/runtime/card_reader64`, `ports/runtime/resource64/nitrofs_*`) | UNKNOWN | A ported host must supply the file API the reconstructed loader expects; the current loader chain is qualified only against synthetic mounts | UNKNOWN on the guest side |
| Sound | **partially proven**: `src/runtime/20261101_word_channels/native_main_0200434c.c` writes channel word `0x04000400 = 0x17` and calls `native_fn_02005994(arg0, 0x04000400)`; the remaining sound registers `0x04000400`-`0x040005ff` appear only in `src/arm7/` and `src/utility/` sources | `u32 (*)(u32 channel_word)` for the proven wrapper; the wider API is UNKNOWN | An ARM9 sound path exists (a channel-register write plus a call into an unidentified SFX routine); the full sound service and its ARM7 coupling are unknown | partially proven |
| Input | no matched source reads `0x04000130`; input handling exists only host-side in `ports/native-host` | UNKNOWN | Guest key/touch reader must be recovered before an input-complete port exists | UNKNOWN |
| Threads/locks | `src/main_sdk_aux/20261101_lock_pair/native_main_02005f08.c`, `20261101_thread_remove124` | lock word acquire/release on a pointer-sized word | Single-threaded ports may no-op only if they never run concurrent guest threads | proven-by-code |
| ARM7 boot handshake | none matched on the ARM9 side; ARM7 images are reconstructed under `src/arm7/` | UNKNOWN | A port must either run the ARM7 image or stub its FIFO status so the ARM9 boot does not spin | UNKNOWN |

## 1a. Whole-image link verification (the gate that keeps this contract honest)

Every claim in this file rests on matched source.  Since this change the tree can *prove* the
matched part of the ARM9 module end to end: `public_tools/whole_image_link.py` compiles every
accepted main-module source, places each function at the address the address ledger measured
for it, links the whole module with the pinned `mwldarm`, and diffs the flat product against
`extract/arm9/arm9.bin`.

* **The linker command file is derived, not written.**  `ports/recompile/arm9.lcf` takes its
  region origins and the five section boundaries from `config/arm9/delinks.txt`, cross-checks
  them against the private module header `extract/arm9/arm9.yaml` (`base_address`,
  `bss_start`, `bss_end`) and the extracted image's size, and follows the Metrowerks LCF
  dialect that `dsd lcf` (dsd 0.12.1) generates for this project.  Each span is
  `. = <measured address>; <object> (.text)`.
* **The diff is byte for byte, and it attributes every difference.**  A difference inside a
  placed function is a gate failure; a difference inside a stubbed function, an alignment hole
  or the `.rodata`/`.data` window is reported as such and cannot pass itself off as a match.
  Placement is proved separately: each placed symbol must sit at its measured address in the
  link product.
* **What it currently proves.**  The linked image is exactly the module's declared 930 560
  bytes, 4 671 functions (440 968 text bytes) are placed, and **4 255 functions / 386 372
  bytes reproduce the extracted bytes exactly** — 44.5 % of `.text`.  That set is committed as
  `ports/recompile/arm9-baseline.json` and CI fails when any member of it stops reproducing.
* **What it does not prove.**  1 791 of 6 463 functions are stubs (424 212 bytes), `.rodata`
  and `.data` are not reconstructed (46 333 bytes), and 417 placed functions declared matched
  by the ledger still differ from the image by 1 691 bytes in total.  The gate reports all
  three rather than papering over them, so no number in this contract should be read as
  "the module is reconstructed".
* **The ROM identity is part of the gate.**  When `inputs/game.nds` is present the tool hashes
  it and fails unless it is the build the ledger and the image came from
  (`674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`).  The ROM is never
  committed and the gate skips cleanly when the pinned private-input bundle is unavailable.
## 2. Porting order

1. **Linkable boot floor** — memory (`CpuSet`/`CpuFastSet`), IRQ save/restore, VBlank/`IntrWait`
   semantics (virtual clock allowed), the boot register draft (`IME`, `POWCNT1`, `DISPCNT`,
   `DISPSTAT`, `0x04000580` — sequence taken from the nonmatching draft, not a matched function),
   heap allocator with the 0-failure contract, FIFO status stub that never reports full, card-bus
   polling stub. This is the minimum to run the boot sequence draft without hanging.
2. **First rendered scene** — display control setter (engine A/B), DMA, the file/card read chain
   (`ports/native-storage` + `ports/native-resources` loader + `ports/native-g3d-assets` decode),
   and the scene/matrix path (`ports/native-scene-matrices`). VRAM/OAM/palette upload is the
   missing piece between "decoded assets" and "pixels".
3. **Game loop** — input reader, sound/ARM7 link, thread/lock semantics, and the ARM7 handshake.
   Until input is recovered the loop can run but cannot be driven.

## 3. What blocks a headless boot today

* No matched guest input reader (KEYINPUT `0x04000130` never referenced in matched source).
* No matched sound API: only one ARM9 channel-register writer is proven
  (`src/runtime/20261101_word_channels/native_main_0200434c.c`); the rest of the sound service and the
  ARM7 handshake are unknown.
* No VRAM/OAM/palette upload path in the native ports; `ports/native-g3d-assets` stops at decoded
  RGBA, and `ports/native-scene-matrices` states rendering is unproven.
* The NitroFS mount/read API on the guest side is unidentified; `ports/native-storage` explicitly
  keeps the mount parser as separate work.
* `native_fn_020042e0` (display control setter) has a proven ABI but unknown identity.
* The `main` entry at `0x02000c34` now has reconstructed source
  (`src/main/p3g_main_02000c34/native_main_02000c34.c`), but the **first calls in its chain are
  still unmatched**: `0x02026b28` (388 B) and `0x020ba490` (212 B), both `functionMatched: false`
  in `ledger/functions.jsonl`. The loop's entry order therefore comes from the reconstructed source,
  not from matched callees.
* ~~No public link path~~ — **closed**: `ports/recompile/` compiles `main()` and `0x020C225C` with the
  pinned `mwccarm`, assembles a minimal `startup.s`, sets `MWLibraries`, and links a flat ARM9 image
  with `mwldarm` (entry `0x02000000`, 1,824-byte ELF / 232-byte flat binary) against an empty stub
  platform layer. The image links but performs no hardware initialisation, because the boot register
  writer `0x02026B28` is still unmatched — that function, not the linker, is now the blocking target.

## 4. Coverage of the existing port work

| port | what it covers | what it does not cover |
| --- | --- | --- |
| `ports/native-host` | Windows/Android window + C11 session, calibration grid, 256x192 viewport input mapping, surface preservation | game assets, DS graphics playback, gameplay; live DPI move untested |
| `ports/native-storage` | guest-address mapper, byte-wise card cache, polling-read transfer, read-only host file provider, 84 host read cases | NitroFS mount parser, renderer, full game; handle sharing needs external serialization |
| `ports/native-resources` | file-backed NitroFS mount, resource loader, bounded arena, dictionary search, texture/palette material setters | current-directory changes, other archives, writes, async scheduling, NARC parsing |
| `ports/native-g3d-assets` | file-backed reads, loader, BMD/BTX framing, MDL0 material associations, TEX0 → RGBA | renderer, VRAM upload, scene execution, playable game |
| `ports/native-scene-matrices` | Q12 matrix commands, node poses, static SBC plans, scene event tapes, per-shape snapshots | rendering, animation, gameplay; cold billboard cache generation and BB8 outside scope |
| `ports/runtime/*` | focused runners/contracts for card reader, cache, NitroFS views, G3D dictionary, texture decode, matrix/pose, stream position | not a complete platform; each component is qualified separately |
| `ports/windows-native`, `ports/android-native` | per-function runners and acceptance harnesses for matched functions | no game loop, no display/audio platform |

## 5. Unknowns (do not invent)

* Guest NitroFS/file API, the wider sound API (only the `0x04000400` channel write is proven), input
  API, ARM7 boot handshake, timers ownership (`0x04000100` block is not referenced by matched main
  code).
* Identity of `native_fn_020042e0` (display control) and the many `native_fn_<addr>` SDK wrappers.
* Whether the two display engines are configured by the same setter path on real hardware or by
  separate ones; the matched caller uses both registers, which is evidence but not proof of a
  single API.
