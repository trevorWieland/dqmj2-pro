# Lens walkthrough — 2026-11-11

Verification that each lens is *served*, not merely present: every step below was executed against
the current tree (`origin/main` `5669d1c5`) with the private inputs, following the documented path
literally. Results are PASS / PARTIAL / FAIL with the exact stopping step and the smallest next
action. RECOMPILATION moved from PARTIAL to PASS the same day once `ports/recompile/` was added;
MOD (data edits) and ROMHACK (text repack) remain PARTIAL by evidence, not by guesswork.

| lens | verdict | stops at | smallest next action |
| --- | --- | --- | --- |
| 1. **MOD** (patch surface) | **PASS** for the documented patch lane; **PARTIAL** for data edits | table byte at file offset `0xD7FE0` is refused (`MISMATCH`) because the ARM9 image is compressed | expose the rebuild lane (`pack_exact.py` + DSProtect serialisation) or document it as the only data path |
| 2. **ROMHACK** (script text) | **PARTIAL** | an edited listing assembles and lands exactly, but there is no container repack step, and listings carry opcodes, not display text | a member→FPK→ROM repack tool, plus recovering the text payload the opcodes reference |
| 3. **RECOMPILATION** (stub platform) | **PASS** (closed 2026-11-11) | links end to end: `ports/recompile/` compiles `main()` + `0x020C225C` + stubs, assembles `startup.s`, and `mwldarm` produces a flat ARM9 image (entry `0x02000000`, 232-byte flat binary) | none for the link path; the next target is the boot register writer `0x02026B28` |
| 4. **ENGINE PORT** (next-needs list) | **PASS** as an inventory deliverable | nothing — the list and the blocking target are identified | recover `0x02026B28` (388 B), the boot register writer |

---

## Lens 1 — MOD: what can a modder change today?

Followed `docs/modding/README.md` + `ops/mod_patch.py` with the documented example spec
(`docs/modding/example-title.json`) against a copy of the measured image.

| step | command | result |
| --- | --- | --- |
| 1. verify | `mod_patch.py --root <scratch> --spec spec.json --check` | `patch 0 0x00000b 1 B ok`; `checksum written 0x83a9`; `header valid after patch`; nothing written, exit 0 |
| 2. apply | same without `--check` | wrote the 175,959,612-byte image, exit 0 |
| 3. verify header | `mod_patch.py --verify-header <output>` | `header valid: logo CRC ok, header CRC 0x83a9, fields in range`, exit 0 |
| 4. contain the change | byte diff input vs output | only `0x00B` (`0x50`→`0x4D`) and `0x15E/0x15F` (header CRC) differ |

**What a modder can change today:** header fields (title, game code, and the rest of the 0x200-byte
header), and any *uncompressed* byte range in the ROM, each guarded by before-bytes and with the
header CRC fixed automatically.

**What a modder cannot change today — measured, not assumed:** a table byte inside the ARM9 image.
`math_table_0x20d3fe0` (runtime `0x020D3FE0`) maps to file offset `0xD7FE0` by the documented formula
(`0x4000 + (A - 0x02000000)`), and a patch there is refused:

```
patch 0  0x0d7fe0  4 B  MISMATCH
image bytes at 0xD7FE0: 6d033859 0d169d00     (table's first word is 10000000)
```

The bytes are not the table — the ARM9 image is stored compressed (607,328 stored → 961,560 bytes),
so the table is not at its runtime address in the file. Data edits therefore need the **rebuild
lane**, which this lens does not document or ship. Monster stats remain unavailable entirely: no
matched reader establishes a per-species stat block, and `species_roster` (`0x021C4BF8`) falls in a
range no captured image covers.

## Lens 2 — ROMHACK: can a romhacker change in-game text today?

Followed `docs/scripts/vm.md` + `scr_disasm.py` / `scr_asm.py` on the documented window
`extract/files/d2_ObjVsTitleData.bin` at `0x50da`, length 99.

| step | command | result |
| --- | --- | --- |
| 1. disassemble | `scr_disasm.py --offset 0x50da --length 99` | `99 byte(s) read, decoded 99 (100.0%), undecoded 0` |
| 2. edit one value | change opcode `0x97 text_target_2_1_1` → `0x99 text_target_2_1_3` in **both** the byte column and the mnemonic | first attempt changed only the byte column and the assembler **refused**: `line 1: listed bytes 99 do not match 97 for 'text_target_2_1_1'` |
| 3. assemble | `scr_asm.py --input edited.txt --output edited.bin` | `wrote 99 bytes`, exit 0 |
| 4. check the edit landed | assembled vs image window | exactly one differing byte: offset `0` is now `0x99` (was `0x97`) |
| 5. round-trip with the edit | `scr_asm.py --roundtrip --input edited.txt --image … --offset 0x50da` | `bytes matched: 98, mismatched: 1`; `first mismatch at 0x000050da: 99 != 97` |

So the decode→edit→assemble loop works and is exactly localised. It is not yet a text mod:

* the listing decodes **opcodes**, not characters. The window is a `text_target_*` command stream;
  the display string the commands select is data the handlers reference, and that payload is not
  located by this lens;
* there is no step that writes the assembled member back into the FPK archive and then into the
  ROM's FNT/FAT container — `scr_asm.py` writes a flat `.bin` and stops.

Verdict **PARTIAL**: a romhacker can change *which* text-VM command runs inside an already-extracted
member, but cannot yet change the text the player reads, and cannot put the result back into the
image. The smallest next action is the container repack path (the project has `pack_exact.py` and
`rom_layout.py` for the rebuild lane; the lens documents neither).

## Lens 3 — RECOMPILATION: a stub platform attempt

Followed `docs/platform/contract.md` §2 step 1 against the tree as it stood *before* the fix below:
`main.c` = the matched `src/main/p3g_main_02000c34/native_main_02000c34.c`, `boot.c` = the matched
boot-floor function `native_main_020c225c.c`, `stubs.c` = a hand-written platform layer implementing
the 16 imported services plus `reset()`.

| step | result |
| --- | --- |
| compile all three units with `mwccarm` | exit 0 each |
| link with `mwldarm` (default LCF) | `Linker command file error at line 23 / File not found: STATICINIT`; `Environment variable 'MWLibraries' not found` |
| link with a hand-written LCF | `Linker command file error at line 8` |

**Original verdict: PARTIAL, stopping at the link step.**

### Closed the same day — `ports/recompile/` (now PASS)

The blocker was four toolchain details, none of them decompilation work:

1. the LCF needs Metrowerks syntax (`#` comments, `>` to allocate a segment and `>>` to append, no
   spaces around `ORIGIN=`/`LENGTH=`), derived from the pinned `test2.lcf`/`ARM9-TEG-C.lcf.template`;
2. `mwasmarm` spells the core `arm5TE`, not `arm946e`;
3. `mwasmarm` rejects local numeric labels and `@` comments;
4. `MWLibraryFiles` is a list of archive names, not a directory, so this flat image must leave it
   unset; `MWLibraries` alone is enough.

`ports/recompile/` now carries `stub.lcf`, `startup.s`, `stubs.c`, `build.ps1` and `build.sh`.
Measured run:

```
compiled  src/main/p3g_main_02000c34/native_main_02000c34.c -> build/recompile/main.o
compiled  src/main/p3g_main_02000c34/native_main_020c225c.c -> build/recompile/boot.o
compiled  ports/recompile/stubs.c -> build/recompile/stubs.o
assembled ports/recompile/startup.s -> build/recompile/startup.o
linked    build/recompile/stub.elf
entry     0x02000000
size      1824 bytes (ELF container)
```

Linked symbols include the matched sources themselves: `main` is `0x0200006c`, 0x50 bytes — the same
80 bytes the ledger measures. `llvm-objcopy -O binary` yields a **232-byte flat ARM9 image**. It
links, it is not the game: no VRAM/OAM upload, no input reader, no sound, no ARM7 image, every
imported service stubbed. **Verdict: PASS** for the link path; the remaining blocker for a *bootable*
image is the unmatched boot register writer `0x02026B28`.

## Lens 4 — ENGINE PORT: what the next porter needs

Grounded in the contract's §1 service catalogue and §2 porting order. A porter arriving today needs,
in this order:

1. **A link script and startup.** Nothing else runs until three objects can become an ELF (lens 3).
2. **The boot register writer, as matched source.** The contract's §1 row "Boot register sequence"
   is currently *draft-derived, not matched*; the function is `0x02026B28` (388 B, ledger
   `functionMatched: false`). Its sequence is the platform floor: `IME = 1`, `POWCNT1` RMW,
   `DISPCNT = 0`, four `DISPSTAT` RMWs, `0x04000580 = 0xBFFF0000`.
3. **The frame dispatcher, as matched source.** `0x020BA490` (212 B, unmatched) is what `main()`
   calls every frame; a port needs it to know what "one frame" means.
4. **The stubbable services**, from the catalogue: IRQ save/restore and `IntrWait` (virtual clock
   allowed), heap allocator with the 0-on-failure contract, ARM7 FIFO status stub that never reports
   full, card-bus polling stub.
5. **The services that cannot be stubbed yet**: guest input reader (`0x04000130`, no matched
   reader), NitroFS/file read API (guest side unknown), sound (one proven channel write only), and
   the ARM7 handshake.
6. **VRAM/OAM/palette upload**, the missing step between the resource subsystem's decoded assets and
   pixels.

**Single blocking decompilation target:** `0x02026B28` — the 388-byte boot register writer. Nothing
in the port can be executed before the platform floor is either matched or explicitly stubbed, and
today it is neither: the contract carries it as a draft, and the function is still unmatched. The
next one, immediately after, is `0x020BA490`.

---

## Notes on method

* Every command above was run against the private inputs on 2026-11-11; outputs are quoted verbatim
  from the terminal, including the failures.
* No lens was marked PASS on the strength of a file existing. The two PARTIAL verdicts are the
  expected outcome: the patch lane and the script round-trip work, the data lane and the text
  repack do not, and the recompilation lane stops at the link step.
