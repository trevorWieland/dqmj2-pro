# Runtime RAM capture

Status: **harness implemented and exercised.** A non-interactive DeSmuME 0.9.13
(Lua) path produces a full `main`-window dump, `ops/ram_capture.py` validates and
slices it, and a real save was driven to the in-game **Switch Monsters** screen.
That screen populated **6 of the 15 roster slots** — exactly the six monsters the
save owns (three party, three reserve). Slots 6-14 are zero because the save has no
more monsters, not because the capture failed. No synthetic bytes are used below;
every number comes from a dump listed in §6.

## Why this exists

`docs/data/unbacked-data.md` proves that some data only exists after the program has
run:

- `species_roster` at **`0x021c4bf8`**, 24-byte records, inside **main BSS**
  (`0x020e3300`–`0x021d7240`, 999,232 bytes, recorded as `expectedBssBytes` in
  `manifest.json`);
- the script VM's **output text block** at **`0x020fb264`**, likewise runtime state
  (`docs/scripts/vm.md` §3: byte cursor at `+0x80`, text array at `0x020fae64`).

BSS is zero-filled at load, so only a dump from a running instance can supply these
bytes, and it must carry provenance or it proves nothing.

## 1. Emulator identity and install

| item | value |
| --- | --- |
| emulator | DeSmuME 0.9.13 x64 SSE2 (Windows frontend) |
| source | `desmume-0.9.13-win64.zip`, official GitHub release `release_0_9_13` |
| URL | https://github.com/TASEmulators/desmume/releases/download/release_0_9_13/desmume-0.9.13-win64.zip |
| zip size / sha256 | 6,086,795 B / `cbf710b8e6b29f0904e289a9b9a895548a2d7c7af5a3145c8279b97a69a09276` |
| executable | `DeSmuME_0.9.13_x64.exe`, 40,140,800 B, sha256 `1ca4e771b92f38a1cef4fc2a61f7d729a638f94d0e56f7948eeeb472000cf32c` |
| install dir | `tools/desmume/0.9.13-win64/` (gitignored) |

The official zip is missing the two Lua runtime DLLs, so Lua scripting cannot run
out of the box (`lua51.dll was not found`). Both are shipped, prebuilt and x64, in
the official **source** release `desmume-0.9.13.tar.xz`
(sha256 `5734450e0c25f442dd44cda6a40410fd65470f4fe2fa1eb9f0b7b6dae22dabaf`), inside
`desmume/src/frontend/windows/lua/lua.7z` under `x64/`:

| file | bytes | sha256 |
| --- | --- | --- |
| `lua51.dll` | 11,776 | `a85ced1c2078348684b74bcc20074f63a73d02881e5dcd002581ed757d8adf86` |
| `lua5.1.dll` | 314,880 | `23719300fa4ae3116e97c313b838945bb2c1e02094daee8165939059aaad82c5` |

Both must sit next to `DeSmuME_0.9.13_x64.exe`. `ops/emulate_capture.py` checks for
them and exits 2 with instructions if absent.

## 2. Non-interactive path (verified)

0.9.13 has **no command-line Lua option** (`--help` lists `--frameskip`,
`--start-paused`, `--load-slot`, `--play-movie`, no Lua, and **no `--disable-gui`**).
The supported automation hook is `[Scripting] AutoLoad` in `desmume.ini`:

1. on ROM load, `OpenCore()` builds `<lua path>\<rom base>.lua`; the default Lua
   path is `<exe dir>\Lua` (`mc.cpp`/`path.cpp` defaults are exe-relative);
2. if the file exists it creates the Lua window and sets `IDC_EDIT_LUAPATH`, which
   fires `EN_CHANGE -> UpdateFileEntered -> PostMessage(IDC_BUTTON_LUARUN)`;
3. the script runs with no keystrokes or mouse clicks.

`tools/desmume/0.9.13-win64/Lua/game.lua` is therefore a one-line shim:

```lua
dofile([[<absolute path to work/emulator/capture.lua>]])
```

This **is displayed on the desktop** — the host has an interactive session
(session 1), and DeSmuME is a GUI application. There is no headless mode for this
frontend. "Non-interactive" here means: no human input is required; the window may
be left in the background, and screenshots are taken by the wrapper via
`CopyFromScreen` while the script has called `emu.pause()`.

Two runtime behaviours cost real debugging time and are load-bearing:

- **Save import.** A bare raw 64 KiB save is read as *empty*: `BackupDevice::readFooter()`
  fails, `_info` is zeroed, `_fsize = 0`, and the game shows no save data. DeSmuME
  `.dsv` = raw bytes + footer:
  `DESMUME_BACKUP_FOOTER_TXT` + `<6 u32 LE: written, padded, type, addr_size, size, version=0>`
  + `|-DESMUME SAVE-|` (122 bytes for this title). 65,536 bytes maps to
  `save_types[3]` = **EEPROM 512kbit**, `addr_size=2`. The wrapper writes this footer.
- **Input injection.** Calling `joypad.set()` from the script's own flow is deferred
  to the next input-processing window and did **not** reach `NDS_getFinalUserInput()`
  in testing (`joypad.get()` stayed empty, no menu movement). Injecting from an
  `emu.registerbefore()` callback works, because that callback runs inside
  `NDS_beginProcessingInput()/NDS_endProcessingInput()`. `capture.lua` does this.
  Button field names are `A,B,X,Y,L,R,start,select,up,down,left,right,debug,lid`
  (lowercase spellings matter; unknown keys are silently ignored). Touch is
  `stylus.set({x=,y=,touch=})`, driven by timeline steps `FRAMES:tap=X,Y`.

## 3. Files

| path | role |
| --- | --- |
| `ops/emulate_capture.py` | wrapper: install checks, scratch copies, `.dsv` import, shim + ini, launch, wait, screenshot, spec, `ram_capture.py` validation/slice, roster report |
| `work/emulator/capture.lua` | authoritative Lua script: warm-up, button/touch timeline, 1,929,792-byte dump, optional savestate save/load, pause/exit |
| `work/emulator/specs/*.json` | capture specs (provenance + ranges) |
| `work/emulator/dumps/*.bin` | raw dumps (gitignored) |
| `ops/ram_capture.py` | validates/slices a dump and emits manifest module entries |

`ops/ram_capture.py` was **missing from `main`** in this checkout (the canonical copy
survived under `work/publish/ops/`); it was restored verbatim before use. The same is
true for the original `docs/data/` tree.

## 4. Working procedure

```powershell
# boot baseline: BSS must be zero; proves the whole pipeline
python ops/emulate_capture.py --name boot --frames 120 --slice

# save -> world -> X menu -> page to "Switch Monsters" -> open the 15-slot list
python ops/emulate_capture.py --name roster-6 --frames 5 --load-state 9 `
  --timeline "100:right;40:;2:A;160:" --slice `
  --screenshot work/emulator/switch-open.png
```

`--load-state 9` is the checkpoint state saved once the X menu is open (see §5 for how
it was reached). Reaching the 15-slot screen from that checkpoint is the reliable
path; the raw menu page sequence is `Items -> Spells and Abilities -> Equipment ->
... -> Switch Monsters` and a held RIGHT advances roughly one page per 20 frames.
The first command is fully reproducible from a cold start; the second reads a local
DeSmuME savestate (`tools/desmume/0.9.13-win64/StateSlots/`), which is not part of
the repository.

Environment variables consumed by `capture.lua`:
`DQM_CAPTURE_OUT`, `DQM_CAPTURE_LOG`, `DQM_CAPTURE_FRAMES`, `DQM_CAPTURE_TIMELINE`,
`DQM_CAPTURE_SAVESTATE`, `DQM_CAPTURE_LOADSTATE`, `DQM_CAPTURE_PAUSE`,
`DQM_CAPTURE_EXIT`, `DQM_CAPTURE_DEBUG` (logs `joypad.get()` readback).

Roster spec used for the validated capture (`work/emulator/specs/roster-6.json`):

```json
{
  "dump": "work/emulator/dumps/switch-open.bin",
  "dumpBase": "0x02000000",
  "module": "main",
  "provenance": {
    "buildSha256": "674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6",
    "tool": "DeSmuME 0.9.13 x64 SSE2 (Windows), Lua 5.1 capture.lua via memory.readbyterange",
    "capturePoint": "save loaded (Akira), X menu -> Switch Monsters screen: 6 of 15 roster records populated (3 party + 3 reserve), 9 slots zero",
    "timestampUtc": "..."
  },
  "captures": [
    {"name": "ram-roster", "address": "0x021c4bf8", "bytes": 360},
    {"name": "ram-scriptvm", "address": "0x020fb264", "bytes": 4096}
  ]
}
```

## 5. What was proved, and what was not

Proved mechanically:

| check | result |
| --- | --- |
| emulator launches the ROM | window title `DeSmuME 0.9.13 x64 SSE2 | DRAGON QUEST MONSTERS Joker2 PROFESSIONAL`; log reports `ROM serial: NTR-B2JJ-JPN` |
| Lua runs with no user input | `[Scripting] AutoLoad` opens the Lua window and runs `capture.lua` |
| dump size/base | exactly 1,929,792 B at `0x02000000` (the whole `main` window) |
| boot baseline | roster slice all zero, `ram_capture.py --check` passes |
| wrong-size dump refused | a 1,929,728-byte dump was rejected with "dump ends … before the module end" |
| save import | title menu shows **Continue** enabled and a real save preview (Akira, 3 monsters, 86:10:48) |
| script VM block | 1,458–1,474 non-zero bytes of 4,096, cursor@+0x80 = 2…25 |
| roster after opening the X menu | 3 of 15 records non-zero: species `263, 403, 403` exactly matching the three party monsters (Nighty, ConkaI, ConkaII) |
| roster after opening **Switch Monsters** | **6 of 15** records non-zero: species `263, 403, 403, 65, 260, 405`; slots 6-14 zero; the screen lists six monsters (3 party + 3 reserve) |
| slicing | `extract/ram/ram-roster_021c4bf8.bin` (360 B, sha256 `cd20f431…4f2a0`), `extract/ram/ram-scriptvm_020fb264.bin` (4,096 B, sha256 `a32af9e0…203f69`), manifest fragment with 2 entries |

**Not proved / not reached:** a 15-of-15 roster. The array capacity is 15
(15 x 24 = 360 B); this save owns six monsters, so six records populate and nine stay
zero. That is a property of the save, not of the capture. Species `263, 403, 65, 260,
405` are outside the ids previously named as "proven" (139/176/188/254/350/425/426);
that set is a predicate for a special sprite in one matched reader, not a species
enumeration, so the mismatch is not evidence against the capture. Field layout of the
six records (species at +0x0A, 800-byte-stride id at +0x04, heap pointers at +0x10/+0x14)
is recorded in `docs/data/species-and-rosters.md`; the 24-byte record is a reference
entry, so level/HP/stats are not in it.

Cold-start navigation is timing-sensitive: an `A` press before the title menu has
finished drawing starts **New Game** instead of Continue (several attempts then show
a long intro with no roster). The menu also ignores `X` while the post-load scene is
still running. Working anchors observed: title menu ready ≈ frame 900–1,200 after
launch; save preview ≈ 240 frames after Continue; world ≈ 700–900 frames after Load;
`X` accepted once the character has moved (e.g. 60 frames of `down`).

A follow-up capture at the same state with --dump-length 4194304 (4 MiB,
0x02000000-0x02400000, work/emulator/dumps/heap-4m.bin) includes the heap and was
used to dereference the record pointers; the stat objects were found outside the
24-byte records, at 0x021bd710 (Nighty) and neighbours. See
docs/data/species-and-rosters.md for the object layout and the equipment caveat.

## 6. Evidence files

| file | bytes | sha256 |
| --- | --- | --- |
| `work/emulator/dumps/boot-wrapper.bin` (boot, zero roster) | 1,929,792 | `23057f29a20bf66526cd3cb0ba563b9a12086b19aed88032ad395b008e79e548` |
| `work/emulator/dumps/menu-open.bin` (3/15 roster, items page) | 1,929,792 | `1d963ea616d1b256e97d5c73be002e5e8d8d3a39fd677133f05305da77e4848d` |
| `work/emulator/dumps/switch-open.bin` (**6/15 roster, Switch Monsters**) | 1,929,792 | `16b4899f1b7393551d147cea1efe2b9744781ea59a21a83c25337b0911ef8d2f` |
| `work/emulator/dumps/roster.bin` (cold-boot attempt, zero roster) | 1,929,792 | `834c3efa2c4527246518ffa0a435002cd3ee3ba0390f71e82d2385dafeff9c67` |

`inputs/game.nds` and `inputs/save.sav` were hashed, copied, and never modified;
the scratch copies under `work/emulator/scratch/` and the emulator's `Battery/`
directory are disposable.

## 7. What remains

1. **Fill all 15 slots.** The 15-slot array and its screen are reached and captured
   (6 records). Filling 15 requires a save that owns 15 monsters; this save owns six.
2. **Cold-start determinism**: the exact frame windows differ per run (see the timing
   note above). The checkpoint-state route used for `roster-6` is deterministic; a
   cold-start script needs the anchors re-confirmed on a quiet host.
3. **Promote the fragment** (integrator step, not done here):

   ```powershell
   # writes a manifest COPY with the two runtime-capture module entries merged in
   python ops/ram_capture.py --spec work/emulator/specs/roster-6.json `
       --apply-manifest build/ram-capture/manifest-with-ram.json
   ```

   `ops/ram_capture.py` refuses to write `manifest.json` itself; the integrator merges
   `build/ram-capture/manifest-modules.json` (2 entries: `ram-roster`, `ram-scriptvm`)
   into the real manifest by hand.
4. Semantic validation of the VM text block (cursor value, text array) — the bytes
   are captured, the decoding is out of scope here.

## 8. Out of scope

- Audio, graphics or save-file extraction beyond the copy needed to load the save.
- Redistributing the ROM, the save, or the dumps; all three stay private/ignored.
- Filling all 15 roster slots: that needs a save with 15 monsters, not a code change.
