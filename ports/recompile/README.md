# Recompilation — from a linked stub to a verified whole-image ARM9 link

This directory is the recompilation lane's link path.  It has two halves:

* a **whole-image link and byte-diff gate** (`arm9.lcf`, `arm9-baseline.json`,
  `public_tools/whole_image_link.py`) that links *every* accepted main-module source file into
  the module's declared section layout and diffs the result against the extracted image;
* the original **minimal stub** (`stub.lcf`, `startup.s`, `stubs.c`, `build.ps1`, `build.sh`)
  that links the two reconstructed boot functions into a 232-byte flat image.

The gate is the part that proves something.  The stub is kept because it is still the only
thing in this tree whose entry point *runs*.

## 1. The whole-image link

### 1.1 What it does

```
public_tools/whole_image_link.py
    ├── reads   config/arm9/delinks.txt        the module's measured section table
    ├── checks  extract/arm9/arm9.yaml         the private module header, must agree
    ├── resolves every src/**/*.c|*.s of the main module through config/source_units.json
    ├── compiles each with the profile its ledger row recorded
    ├── pairs each compiled function with the address ledger's row for it
    ├── writes  ports/recompile/arm9.lcf       one `. = <address>; <object> (.text)` per span
    ├── writes  an absolute symbol carrier     every measured name -> its measured address
    ├── links   with mwldarm through a response file (4 700+ objects)
    └── diffs   the flat product against extract/arm9/arm9.bin, byte for byte
```

The linker writes the ARM9 region straight to a flat binary (`MEMORY { ARM9 : ORIGIN = 0x… >
arm9.bin }`), so the link product *is* the module image — no `objcopy` step, no ELF container
to explain away.  Its length is fixed by the final location-counter assignment in the
`.arm9` section, and the tool fails if it is not exactly the module's declared size.

### 1.2 The command

```powershell
# from the repository root, with the pinned toolchain and the private inputs present
python public_tools/whole_image_link.py --root . --out build/whole-image --jobs 12

# regenerate the committed linker command file
python public_tools/whole_image_link.py --root . --emit-lcf

# prove the committed linker command file is current
python public_tools/whole_image_link.py --root . --check-lcf

# refresh the reproducible-function baseline
python public_tools/whole_image_link.py --root . --emit-baseline

# no private inputs needed: validate the section table and derived geometry
python public_tools/whole_image_link.py --root . --check-layout
```

In CI the private inputs arrive exactly the way the authored-code build gets them
(`.github/workflows/whole-image-link.yml`): the pinned `dqmj2-pro-inputs` repository is
checked out into `private-inputs/` with `BUILD_INPUTS_DEPLOY_KEY`, and `--input-bundle
private-inputs` installs `extract/`, `ledger/` and `tools/` into the checkout through
`build_bytematch.install_bundle`.  Nothing private is committed.  If the bundle is absent the
tool prints `skipped-missing-inputs` and exits zero, so a fork without the key stays green.

Outputs land in `build/whole-image/` (gitignored): `arm9.bin` (the linked image),
`arm9.elf`, `arm9.lcf`, `abs.s`, `plan.json`, `objects.rsp`,
`summary.json`, and `link.json` on failure.

### 1.3 Where every number in `arm9.lcf` comes from

`ports/recompile/arm9.lcf` is generated and carries its provenance in its header.  Nothing in
it is typed by hand.

| directive | source |
| --- | --- |
| `MEMORY { ARM9 : ORIGIN = 0x02000000 > arm9.bin }` | `.text` start in `config/arm9/delinks.txt`, cross-checked against `base_address` in `extract/arm9/arm9.yaml` |
| written length `0x0e3300` | `.data` end == `.bss` start in the section table; also the size of `extract/arm9/arm9.bin` |
| `MEMORY { BSS : ORIGIN = 0x020e3300 }` | `.bss` start; the region names no output file, so `.bss` is reserved but never written |
| `. = 0x02000000` / `0x020d3fe0` / `0x020dcb30` / `0x020dcb40` / `0x020e3300` | the five section boundaries in the section table |
| `ALIGNALL(2)` | 13 of the module's functions start at a 2-mod-4 address; a 4-byte floor would move every Thumb function two bytes past its measured address |
| final `. = 0x020e3300` | `.data` end; this is what fixes the binary's length |
| `. = <addr>; <obj> (.text)` | one line per placed function; `<addr>` is the ledger row's measured address, `<obj>` is the object compiled for that source and profile |
| dialect (`MEMORY … > file`, `AFTER`, `ALIGNALL`, `. = 0x…`, `WRITEW`, `KEEP_SECTION`, `* (.section)`, `object.o (.section)`) | the `dsd lcf` output dsd 0.12.1 generates for this project — the same Metrowerks LCF dialect the pinned mwldarm accepts |

The section table is committed, so the layout half of the file is reproducible from public
data alone.  A function with no reconstructed source is *not* placed: the linker leaves zero
bytes in the hole, the next span keeps its absolute address, and the diff reports the hole.
Nothing is copied from the image, so a hole cannot fake a match.

Two linker facts cost real debugging and are worth knowing:

* **`-nodeadstrip` is required.**  Without it mwldarm silently drops every placed section that
  nothing references, and the region comes out empty.
* **Object files can only be named by bare file name in the LCF.**  `objects/foo.o` makes the
  parser report `File not found: objects`, so every object lives flat beside the command file
  and the linker runs with that directory as its working directory.

### 1.4 What the diff proves

The gate compares all 930 560 bytes of the linked image with all 930 560 bytes of
`extract/arm9/arm9.bin` and attributes every difference to an owner:

* **reconstructed span** — a placed function.  Any difference here means the gate fails.
* **stub row** — a ledger function with no placed source.  Expected to differ.
* **text hole** — bytes the delinker did not attribute to a function (alignment padding).
* **data window** — `.rodata` / `.ctor` / `.data`, which are not reconstructed at all yet.

It also proves placement independently: every placed span's symbol must sit at its measured
address in the link product's symbol table, and a displaced symbol fails the gate.

The repository commits `ports/recompile/arm9-baseline.json`, the set of functions the gate has
already proved byte-exact.  The pass condition is: the image is the declared size, no function
is displaced, **no baseline function left the set**, and the reproduced byte count did not
fall.  That makes the gate a regression gate over a proven set rather than a claim about the
whole module, and it means a new source that does not reproduce cannot silently appear to.

### 1.5 Measured result

Run on this tree with the pinned `mwccarm`/`mwasmarm`/`mwldarm` from
`tools/mwccarm/mwccarm/2.0/base`:

```
module                       main (ARM9), base 0x02000000
declared image               930560 bytes  (.text 868320 + .rodata 35664 + .data 26560)
linked image                 930560 bytes  exact
source units resolved        5803 C + 52 assembly = 5855
compiled / assembled         5832        failed 23
spans placed                 4671        text covered 440968 bytes
absolute symbols carried     15363       name/address conflicts 145
reproduced exactly           4255 functions / 386372 bytes
residual (placed, differs)   417 spans / 1691 bytes
ledger functions stubbed     1791 rows / 424212 bytes
text holes                   1034 runs / 3140 bytes
data window                 46333 bytes, not reconstructed
```

So **386 372 of the module's 868 320 text bytes (44.5 %) link to the extracted bytes exactly**,
and every one of them is recorded in the baseline so the result cannot quietly regress.

### 1.6 What this does *not* prove — the honest limits

* **Stubs are not the game.**  1 791 of the module's 6 463 functions are placeholders: the
  linker leaves zeros in their space.  The image links and is the right size; it is not the
  module.
* **`.rodata`, `.ctor` and `.data` are not reconstructed.**  46 333 bytes of the image are
  therefore zero in the link product.  Any reconstructed function that reads a literal pool
  only it owns can still differ, because that data lands in the window's start rather than at
  its original address.
* **The residual 1 691 bytes is real.**  417 placed functions are declared matched by the
  ledger but do not reproduce from the current source, mostly by 2–8 bytes.  They are listed
  in `summary.json` under `diff.mismatched`, with the source path for each, and they are the
  next work item rather than something the gate hides.
* **40 source files cannot be placed at all.**  A source that defines several functions at
  non-contiguous addresses (`src/save_accessors.c` alone owns 34 rows spread across the
  module) compiles to one contiguous `.text`, and one object cannot be placed in several
  places.  These are reported as `inconsistentUnits` and their rows stay stubs.
* **Not every accepted source compiles here.**  23 units fail to compile with the pinned
  compiler and are reported in `summary.json` under `failures`.
* **The ROM is an identity, not a reproduction.**  When `inputs/game.nds` is present the tool
  hashes it and fails the gate unless it is the build both the ledger and the image came from
  (`674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`, 175 959 612 bytes).
  The gate does not rebuild the ROM: the ARM9 module is the unit under test.

### 1.7 Files

| file | purpose |
| --- | --- |
| `arm9.lcf` | **generated** whole-image linker command file: MEMORY regions, the five section boundaries, 4 671 absolute placements, and the provenance of every number. Regenerate with `--emit-lcf`; CI fails if it is stale. |
| `arm9-baseline.json` | **generated** set of functions that link to the extracted bytes exactly: `[[address, symbol, bytes], …]` plus the image and section-table hashes. This is the gate's reference. |
| `stub.lcf` | the minimal one-region linker command file for the stub image. |
| `startup.s` | stub entry `__startup`: sets `sp`, masks IRQ/FIQ, copies `.data`, zeroes `.bss`, calls `main`, hangs. |
| `stubs.c` | the 16 services the stub's `main()` imports, all returning zero. |
| `build.ps1` / `build.sh` | build the stub image. |

## 2. The stub image (unchanged)

`build.ps1` / `build.sh` compile the two matched boot functions, a stubbed platform layer and
`startup.s`, and link them with `stub.lcf` into a flat ARM9 ELF whose entry point is
`0x02000000` and whose `llvm-objcopy -O binary` form is 232 bytes.  It proves the toolchain
path end to end and gives a porter a runnable starting point; it is not the game.

```powershell
pwsh -NoProfile -File ports/recompile/build.ps1
pwsh -NoProfile -File ports/recompile/build.ps1 -Toolchain <path-to>/mwccarm/2.0/base
```

```bash
./ports/recompile/build.sh [toolchain-dir] [out-dir]
```

### Toolchain notes worth knowing

* **`MWLibraryFiles` is a list of archive file names, not a directory.** Pointing it at the
  toolchain directory produces `Specified file 'C' not found` (the value splits on the drive
  colon). Both stub scripts leave it unset; the linker prints a harmless warning.
* **The assembler spells the core `arm5TE`.** `-proc arm946e` is accepted by `mwccarm` but
  rejected by `mwasmarm`.
* **LCF syntax is Metrowerks-specific.** Comments are `#`, the first section allocates a
  segment with `>` and later sections append with `>>`, and `ORIGIN`/`LENGTH` need no spaces
  around `=`.
* **`mwasmarm` rejects local numeric labels** (`1:`, `5b`); use named labels.
* **The linker defaults to `__startup` as the entry symbol**, which is why both `startup.s`
  and the whole-image symbol carrier define it.
* **Absolute symbols need `.global`.**  `name = 0xADDR` alone produces a *local* absolute
  symbol that resolves nothing; the whole-image carrier emits `.global name` before each
  assignment, which is why it assembles to a multi-hundred-kilobyte object.

## 3. What is still blocking a *bootable* image

The contract's §2 porting order still lists the real boot register sequence as unmatched: the
function at `0x02026B28` (388 B) writes `IME`, `POWCNT1`, `DISPCNT`, four `DISPSTAT` RMWs and
`0x04000580`.  The stub deliberately does not invent that sequence, and the whole-image link
leaves it a stub row like every other unmatched function.  It remains the single
highest-value decompilation target for this lane.
