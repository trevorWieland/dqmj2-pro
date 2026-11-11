# Platform contract — hardware/SDK boundary of the matched ARM9 code

Status: evidence report plus a declaration-only interface header (`include/platform.h`). No build
target is added. Everything below is derived from matched source in this checkout; each item cites
the file and function. Items without a matched reader are marked **UNKNOWN** and are not invented.

## 0. Method and evidence limits

* `config/arm9/symbols.txt` has 7,988 symbols but only ~20 carry SDK names; the rest are
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
* No matched main-module reader was found for the NitroFS file API, sound, input, or the ARM7 boot
  handshake. Those services are **UNKNOWN** and are listed as blockers rather than modelled.

## 1. Service catalogue

| service | matched evidence (file → function) | ABI shape | hardware/SDK assumption a port must satisfy | confidence |
| --- | --- | --- | --- | --- |
| IRQ save/restore | `src/runtime/20261101_fifo_send136/native_main_0200a440.c` (brackets the FIFO write with `native_fn_02007ff4` / `native_fn_02008008`); `src/itcm/restart.c` (`native_itcm_01ff81b4` clears `0x04000208`) | `u32 (*)(void)` returns prior IME; `void (*)(u32)` restores | A maskable IRQ source with the DS IME/IE/IF block at `0x04000208`-`0x04000214` | proven-by-code (register block INFERRED from DS map) |
| VBlank/IRQ wait | `src/hardware/bootstrap_bios/native_main_bios_020002ae.s` (`IntrWait`), `020003e6.s` (`VBlankIntrWait`) | `(u32 discard, u32 mask)` / `(u32 discard, u32 state)` | Vertical-blank IRQ must be deliverable; a headless port needs a virtual clock or VBlank pump | proven-by-code (symbol name + matched asm) |
| Boot register sequence | `src/main/p1e_main_02026b28/native_main_02026b28.c` | `void (*)(void)` | Write order: IME=1, POWCNT1 `0x04000304` mask `0xfffffdf1|0xe|0x200`, DISPCNT `0x04000050`=0, four DISPSTAT `0x04000060` RMWs, `0x04000580`=0xbfff0000, then subsystem inits | proven-by-code |
| Display control | `src/runtime/runtime03/native_main_02041774.c` calls `native_fn_020042e0(0x04000050, mode, flag)` and `(0x04001050, …)` for engine B | `(u32 register, u32 mode, u32 flag)` | A DISPCNT-like register at `0x04000050` and engine-B at `0x04001050`; setter name `native_fn_020042e0` is UNKNOWN | ABI proven, setter identity INFERRED |
| DMA | `src/itcm/dma.c` (`native_itcm_01ff8448`, `-8488`, `-84f8`, `-851c`) | `(s32 channel, u32 src, u32 dst, u32 control)` | Registers `0x040000b0 + channel*12` = SAD/DAD/CNT; channel 0 reads SAD twice as a write barrier; control `0x81400001` for immediate copy | proven-by-code |
| CPU copy/fill | matched callers of `CpuSet` `0x0200064a` and `CpuFastSet` `0x020007a6` (named SDK symbols) | `(const void *src, void *dst, u32 control)` | Fill vs copy selected by argument bit; word/halfword unit selected by control | proven-by-code (bit semantics INFERRED) |
| Heap/alloc | `src/ov006/p1k_ov006_thumb/native_main_021f1f0c.c` allocates through vtable `0x0221aad0 + 0x04` and zero-fills; `src/main_sdk_aux/20261101_frame_heap_core324`, `20261101_heap_search356`, `20261101_heap_attribute424` | `void *(*)(u32 bytes)`; 0 on failure; block headers 0x18 bytes seen in heap sources | A two-level heap (arena, attribute, search) with the same failure contract; host malloc is acceptable if sizes/headers are preserved | alloc contract proven; free path INFERRED |
| ARM7 IPC FIFO | `src/runtime/20261101_fifo_send136/native_main_0200a440.c` | `s32 (*)(u32 channel, u32 payload, u32 flag)`; 0 ok, -1 full, -2 send-empty | Word layout `channel:5, flag:1, payload:26`; status `0x04000184` bit14 full/bit1 empty; data `0x04000188` | proven-by-code |
| Card command bus | `src/mechanics_save/20261029_card_command.c` | `(u32 first, u32 second)`; control `0xc0`, 8 command bytes at `0x040001a1`; poll `0x040001a4` bit31 | Raw card bus, not the NitroFS read API | proven-by-code |
| NitroFS/file read API | none matched in main source; host side only (`ports/native-storage`, `ports/runtime/card_reader64`, `ports/runtime/resource64/nitrofs_*`) | UNKNOWN | A ported host must supply the file API the reconstructed loader expects; the current loader chain is qualified only against synthetic mounts | UNKNOWN on the guest side |
| Sound | no matched main-module source; sound registers `0x04000400`-`0x040005ff` appear only in `src/arm7/` and `src/utility/` sources | UNKNOWN | Presumably crosses the FIFO to the ARM7 sound driver, but no matched main-side caller exists | UNKNOWN |
| Input | no matched source reads `0x04000130`; input handling exists only host-side in `ports/native-host` | UNKNOWN | Guest key/touch reader must be recovered before an input-complete port exists | UNKNOWN |
| Threads/locks | `src/main_sdk_aux/20261101_lock_pair/native_main_02005f08.c`, `20261101_thread_remove124` | lock word acquire/release on a pointer-sized word | Single-threaded ports may no-op only if they never run concurrent guest threads | proven-by-code |
| ARM7 boot handshake | none matched on the ARM9 side; ARM7 images are reconstructed under `src/arm7/` | UNKNOWN | A port must either run the ARM7 image or stub its FIFO status so the ARM9 boot does not spin | UNKNOWN |

## 2. Porting order

1. **Linkable boot floor** — memory (`CpuSet`/`CpuFastSet`), IRQ save/restore, VBlank/`IntrWait`
   semantics (virtual clock allowed), the boot register model (`IME`, `POWCNT1`, `DISPCNT`,
   `DISPSTAT`, `0x04000580`), heap allocator with the 0-failure contract, FIFO status stub that
   never reports full, card-bus polling stub. This is the minimum to link and run
   `native_main_02026b28` without hanging.
2. **First rendered scene** — display control setter (engine A/B), DMA, the file/card read chain
   (`ports/native-storage` + `ports/native-resources` loader + `ports/native-g3d-assets` decode),
   and the scene/matrix path (`ports/native-scene-matrices`). VRAM/OAM/palette upload is the
   missing piece between "decoded assets" and "pixels".
3. **Game loop** — input reader, sound/ARM7 link, thread/lock semantics, and the ARM7 handshake.
   Until input is recovered the loop can run but cannot be driven.

## 3. What blocks a headless boot today

* No matched guest input reader (KEYINPUT `0x04000130` never referenced in matched source).
* No matched sound API on the ARM9 side; the ARM7 handshake is unknown.
* No VRAM/OAM/palette upload path in the native ports; `ports/native-g3d-assets` stops at decoded
  RGBA, and `ports/native-scene-matrices` states rendering is unproven.
* The NitroFS mount/read API on the guest side is unidentified; `ports/native-storage` explicitly
  keeps the mount parser as separate work.
* `native_fn_020042e0` (display control setter) has a proven ABI but unknown identity.
* The reconstructed `main` at `0x02000c34` is not in matched source yet, so the exact call order of
  the loop is currently read from disassembly, not from matched code.

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

* Guest NitroFS/file API, sound API, input API, ARM7 boot handshake, timers ownership
  (`0x04000100` block is not referenced by matched main code).
* Identity of `native_fn_020042e0` (display control) and the many `native_fn_<addr>` SDK wrappers.
* Whether the two display engines are configured by the same setter path on real hardware or by
  separate ones; the matched caller uses both registers, which is evidence but not proof of a
  single API.
