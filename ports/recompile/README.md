# Recompilation stub — a public link path for the reconstructed boot floor

This directory closes the first concrete blocker found by the lens walkthrough: the public tree
could compile matched source but had no way to link it. `build.ps1` / `build.sh` now compile the two
matched boot functions, a stubbed platform layer and a minimal startup, and link them with the
pinned `mwldarm` into a flat ARM9 ELF.

**What this is:** a linked image whose entry point (`0x02000000`) executes the reconstructed
`main()` from `src/main/p3g_main_02000c34/native_main_02000c34.c` against empty services. It proves
the toolchain path end to end and gives a porter a linkable starting point.

**What this is not:** the game. There is no VRAM/OAM upload, no input reader, no sound, no ARM7
image, no file API. Every imported service returns zero or does nothing. Running it on hardware or
an emulator would enter `main()`'s loop and spin; the point is that it links, not that it boots a
game.

## Files

| file | purpose |
| --- | --- |
| `stub.lcf` | minimal linker command file: one `RWX` region at `0x02000000`, `.text`/`.data`/`.bss` in load order, linker symbols for the startup loops. Every directive is commented with where it came from. |
| `startup.s` | entry `__startup`: sets `sp`, masks IRQ/FIQ (CPSR bits 7/6), copies `.data`, zeroes `.bss`, calls `main`, then hangs. Justified assembly — the game's own startup is not recovered, and the boot register sequence (`0x02026B28`) is deliberately not faked here. |
| `stubs.c` | the 16 services `main()` and `0x020C225C` import, plus the two data blobs they touch. Two return values are chosen so the boot loop takes its early path. |
| `build.ps1` | Windows build: resolves the toolchain, sets `MWLibraries`, compiles/assembles/links, prints entry and size. |
| `build.sh` | POSIX twin of the same steps. |

## Usage

```powershell
# from the repository root, with the pinned toolchain present at the default path
pwsh -NoProfile -File ports/recompile/build.ps1

# or point at any checkout that has the pinned toolchain
pwsh -NoProfile -File ports/recompile/build.ps1 -Toolchain <path-to>/mwccarm/2.0/base
```

```bash
./ports/recompile/build.sh [toolchain-dir] [out-dir]
```

Outputs under `build/recompile/` (gitignored): `main.o`, `boot.o`, `stubs.o`, `startup.o`,
`stub.elf`.

## Measured result

Run with the pinned `mwccarm`/`mwasmarm`/`mwldarm` from `tools/mwccarm/mwccarm/2.0/base`:

```
compiled  src/main/p3g_main_02000c34/native_main_02000c34.c -> build/recompile/main.o
compiled  src/main/p3g_main_02000c34/native_main_020c225c.c -> build/recompile/boot.o
compiled  ports/recompile/stubs.c -> build/recompile/stubs.o
assembled ports/recompile/startup.s -> build/recompile/startup.o
linked    build/recompile/stub.elf
entry     0x02000000
size      1824 bytes (ELF container)
```

The linked symbols are the matched sources themselves:

```
02000000 g F code 00000054 __startup
0200006c g F code 00000050 main          ; 80 bytes, the measured size of main()
```

`llvm-objcopy -O binary` turns the ELF into a **232-byte flat ARM9 image** (code + literal pools;
the ELF container adds headers). That image is the smallest thing this project can hand to a port:
a real, linked `main()` loop with no platform behind it.

## Toolchain notes worth knowing

* **`MWLibraryFiles` is a list of archive file names, not a directory.** Pointing it at the
  toolchain directory produces `Specified file 'C' not found` (the value splits on the drive colon).
  This flat image links no Metrowerks runtime, so both scripts leave it unset; the linker prints a
  harmless `Environment variable 'MWLibraryFiles' not found` warning.
* **The assembler spells the core `arm5TE`.** `-proc arm946e` is accepted by `mwccarm` but rejected
  by `mwasmarm` (`Unknown option 'arm946e'; expected one of 'arm4, … arm5TE, …'`).
* **LCF syntax is Metrowerks-specific.** Comments are `#` (a `/* */` block makes the parser report
  `Expecting: MEMORY` at line 2), the first section allocates a segment with `>` and later sections
  append with `>>` (`Segment code already allocated` otherwise), and `ORIGIN`/`LENGTH` need no
  spaces around `=` (the working `test2.lcf` in the toolchain directory is the shape that parses).
* **`mwasmarm` rejects local numeric labels** (`1:`, `5b`); named labels are used throughout
  `startup.s`.
* **The linker defaults to `__startup` as the entry symbol**, which is why `startup.s` defines it.

## What a person can do with the result

* Link new reconstructed functions into a growing image and see the real object code the pinned
  compiler produces at their measured addresses.
* Use it as the skeleton for a port: replace `stubs.c` with real service implementations one at a
  time, and watch which of `main()`'s imports move from stub to real.
* Diff the compiled bytes of `main()` and `0x020C225C` against the image (the build uses the same
  profile the ledger records), which is how the next functions get accepted.

## What is still blocking a *bootable* image

The contract's §2 porting order still lists the real boot register sequence as unmatched: the
function at `0x02026B28` (388 B) writes `IME`, `POWCNT1`, `DISPCNT`, four `DISPSTAT` RMWs and
`0x04000580`. This stub deliberately does not invent that sequence, so the image links but cannot
initialise the platform. That function remains the single highest-value decompilation target for
this lane.
