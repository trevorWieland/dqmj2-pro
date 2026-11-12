# The jump-table carrier: data inside a measured extent, 66 rows / 42,976 B

Status: adopted 2026-11-12. This document is the rule; `ops/transcribe_data_rows.py`
is the generator and `ops/verify_data_rows.py` is the gate.

The aggregate-copy and sweep lanes leave a row unscheduled when its measured
extent is code **plus data**: an inline dispatch table, a reciprocal table, or a
literal pool that a compiler would deduplicate. The ordinary transcription form
(one `asm` body of instructions, `ldr rX, =word` pool loads) cannot express
those bytes. This lane resolves the tooling limit, ships 66 such rows, and pins
the convention.

| population | rows | bytes |
| --- | ---: | ---: |
| unclaimed `ov006` rows whose extent contains a provable inline table | 64 | 41,320 |
| `main` rows with a 256-byte reciprocal table between two code bodies | 2 | 2,300 |
| **shipped** | **66** | **42,976** |

All 66 rows are byte- and relocation-exact: 2,098 pinned relocations, 70 pinned
pool words, four section-alignment pad bytes, one mutated-source negative control
per row, **0 failures**.

## What the carrier is

The extent is emitted as an ordered sequence of **code and data segments**, not
as one instruction run with a trailing pool:

* ARM rows (**23**: 21 `ov006` + 2 `main`) are one mwccarm `asm` translation
  unit. Data runs — the inline table and every literal pool — are `dcd`
  directives. A pool load keeps the measured `ldr rX, [pc, #imm]` instruction,
  so the assembler does not own the pool layout and cannot deduplicate two slots
  that the image keeps separate. A data word that names an address is
  `dcd native_fn_<addr>` / `dcd native_data_<addr>` with its measured addend; an
  odd Thumb function pointer keeps its `+1`.
* Thumb rows (**43**) are one mwasmarm `.s` translation unit. Their switch
  tables are 16-bit entries that begin at 2-mod-4 addresses, which no 32-bit
  directive can express; the table is `.hword` data and each literal pool word is
  `.word` data under a `.L_pool_<addr>` label. Instructions, `.extern` symbols,
  `bl`/`blx` and local labels are mwasmarm syntax (non-suffixed `mov`/`add`/`lsl`
  forms, conditions after the mnemonic).

The two carriers are not a style choice: `dcd` is the only data directive
mwccarm's inline assembler accepts, and it writes 32 bits. A 16-bit table at a
2-mod-4 address therefore cannot use it.

## The falsifier: every spelling, and the exact error

One spelling per translation unit, compiled with the pinned toolchain. The
diagnostics are the tool's own first line.

| carrier | spelling | result |
| --- | --- | --- |
| mwccarm `asm` | `dcd 0x12345678` | **accepted**, emits `78 56 34 12` |
| mwccarm `asm` | `.word 0x12345678` | rejected: `unknown assembler instruction mnemonic` |
| mwccarm `asm` | `.long 0x12345678` | rejected: `unknown assembler instruction mnemonic` |
| mwccarm `asm` | `.4byte 0x12345678` | rejected: `invalid floating-point constant` |
| mwccarm `asm` | `.byte 0x12` | rejected: `unknown assembler instruction mnemonic` |
| mwccarm `asm` | `.hword 0x1234` | rejected: `unknown assembler instruction mnemonic` |
| mwccarm `asm` | `.short 0x1234` | rejected: `unknown assembler instruction mnemonic` |
| mwccarm `asm` | `dc32 0x12345678` | rejected: `unknown assembler instruction mnemonic` |
| mwccarm `asm` | `dc.b 0x12` | rejected: `unknown assembler instruction mnemonic` |
| mwccarm `asm` | `dc.w 0x1234` | rejected: `unknown assembler instruction mnemonic` |
| mwccarm `asm` | `dc.l 0x12345678` | rejected: `unknown assembler instruction mnemonic` |
| mwccarm `asm` | `dcd 0x1, 0x2` | rejected: `end of line expected` (one value per line) |
| mwccarm `asm` | `dcd <local label>` | rejected: `illegal constant expression` |
| mwccarm `asm` | `dcd <extern symbol>` | **accepted**, emits `R_ARM_ABS32` |
| mwasmarm `.s` | `.word 0x11223344` | **accepted**, 4 bytes |
| mwasmarm `.s` | `.word sym` / `.word sym+4` | **accepted**, relocation / addend |
| mwasmarm `.s` | `.hword 0x003e` / `.short 0x003e` | **accepted**, 2 bytes |
| mwasmarm `.s` | `.byte 0x12` | **accepted**, 1 byte |
| mwasmarm `.s` | `dc.b` / `dc.w` / `dc.l` / `dcd` | rejected: `Undefined macro or opcode: dc.w` (and siblings) |

Two mwasmarm details matter and are pinned by tests:

* `.text` is padded to a 4-byte boundary. `.size` is exact, so a 2-mod-4 extent
  gets up to three trailing zero bytes **after** the symbol; they are section
  alignment, not extent. The verifier allows at most three, requires them to be
  zero, and checks the symbol size against the ledger's `bytes`.
* `.hword`/`.byte` are accepted; an ARM instruction that follows unaligned data
  is a hard error (`ARM instruction must be 4-byte aligned`). The two `main`
  tables are 256 bytes, so the following ARM code stays aligned; the Thumb lane
  needs no alignment because Thumb instructions are 2-byte aligned.

## Build-path accounting (what “counted” means for a `.s`)

* `public_tools/source_units.py` enumerates every `.s` under `src/` as an
  `assembly` unit (`kind: s`), resolves it through the same rule chain as C, and
  `--check` counts it. A lane rule fragment is enough; no build-path change is
  needed.
* `public_tools/repo_build.py` compiles a non-C unit only when a **ledger row's
  `sourceUnit` names that file** and supplies `compilerFlags` /
  `compilerSha256`; otherwise the unit is recorded as `unattributed` and is not
  compiled. The project's established `.s` identity is
  `tools/mwccarm/mwccarm/2.0/base/mwasmarm.exe`
  (`e928cbcce71d687fadf25cf426280f23252e2aaae897fc2ce4e5570d8554dc8c`) with
  `-proc arm5TE -c`. A `.s` lane is therefore not “counted” by the build until
  the ledger row is updated to that identity; the lane itself ships the source,
  the rule fragment and the verifier.
* `public_tools/whole_image_link.py` assembles every `main` `.s` with mwasmarm,
  pairs `native_main_<addr>` by its address-bearing symbol, and places the
  object at the measured span. The two `main` rows in this lane could therefore
  also be exercised by the whole-image link; they are shipped here through the
  `dcd` carrier instead, and their bytes are proved by `ops/verify_data_rows.py`.
* A `.s` unit carrying data inside the measured extent is **already** an accepted
  shape, not a new build concept. `src/itcm/hardware/native_itcm_01ff8000.s`
  (88 B) ends with two `.word` pool slots at +80/+84 and
  `native_itcm_01ff8058.s` (348 B) ends with four at +332..+344; both ledger rows
  name that `.s`, the mwasmarm identity
  `e928cbcce71d687fadf25cf426280f23252e2aaae897fc2ce4e5570d8554dc8c` and
  `-proc arm5TE -c`, and both are `functionMatched`/`moduleLinked`. The lane
  extends that accepted `.s` shape to 16-bit tables and explicit 32-bit pools.
* The ledger extent **includes** the data: `main:0x02025578` is 952 B
  (180 code + 256 table + 516 code), `main:0x0202654c` is 1,348 B (312 + 256 +
  780), and each Thumb row's `bytes` covers its table and pools. A verifier that
  compared only the code would accept a short object; this lane's verifier
  compares the whole extent.

## The class, corrected

The 2026-11-12 sweep note says all 69 pc-writing rows contain a table “that an
instruction transcription could not match”. Measured row by row, that is true
for the Thumb shape and false for the ARM shape:

* ARM `addls pc, pc, rN, lsl #2` is followed by **branch words**. Each entry is
  a real `b target` instruction with an in-row target, so the instruction stream
  is transcribable. This lane still emits those words as `dcd` data because the
  measured extent is data between code bodies (and because the same carrier
  removes the duplicate-pool limit); the bytes are identical either way.
* Thumb `add rD, pc; ldrh rD, [rD, #6]; lsl; asr; add pc, rD` is followed by
  **signed 16-bit offsets**, added to the dispatch's `pc + 4`. They are data:
  decoding them as instructions does not reproduce the offset values.

After #192 shipped 118 `ov006` rows, 64 of the 69 remain unclaimed; all 64 have
a provable inline table (the other five are now defined in `src/`). Three rows
exceed the 2,000-byte lane cap that earlier passes used (5,728 B, 9,704 B and
2,584 B) and are shipped here because the carrier is extent-based, not
cap-based.

## The duplicate-literal limit does not bind this carrier

The earlier lanes refused a row when the image keeps the same small constant in
two pool slots, because `ldr rX, =constant` deduplicates one expression into one
slot and the row comes out short. The explicit-pool carriers do not have that
failure: a pool load stays the measured `ldr rX, [pc, #imm]` (ARM) or a
`.L_pool_<addr>` load of an explicitly placed `.word` (Thumb), so every measured
slot exists whether or not its value repeats.

Six of the 66 rows keep two or more **distinct** slots with the same word — a
data address (`0x220cb88`, `0x2216940`, `0x2219b4c`, `0x2219b50`, `0x220d3dc`,
`0x221a960`, `0x221aad0`), a constant (`0xff7`, `0x116`, `0x121`, `0xffff`,
`0x5790`). Four ARM rows were refused by the old transcriber for exactly this
shape (`0x21d8874`, `0x21dc3b8`, `0x21dfa24`, `0x21e0454`) and ship here. The
refusal was a property of the `=constant` spelling, not of the row.

## Worked example

`ov006:0x021ee600`, 104 B, Thumb. The ledger extent is code + a 9-entry table +
an 8-byte pool. The generated unit is
`src/verified_assembly/20261112_jumptable_carrier/ov006/thumb/native_ov006_021ee600.s`:

```
.section .text
.thumb
.extern native_fn_02089d8c
...
native_ov006_021ee600:
    push {r3, lr}
    ldr r1, .L_pool_021ee660
    ldr r0, [r1, #0x18]
    cmp r0, #0x8
    bhi .L_021ee656
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x003e        @ nine offset entries, 0x21ee616..0x21ee627
    ...
    bl native_fn_02089d8c
    ...
.L_pool_021ee660:
    .word 0x0221aa80     @ a data address outside ov006: kept numeric, not guessed
    .word native_fn_021ee348+1
.size native_ov006_021ee600, .-native_ov006_021ee600
```

The table starts at `0x21ee616` (2-mod-4); `dcd` cannot write there, `.hword`
can. A `main` row uses the other carrier: `native_main_02025578.c` is one `asm`
function whose 256-byte table is 64 `dcd 0x...` lines between the two code
bodies, with the measured `sub r0, pc, #148` and the code's own `ldr [pc, #n]`
loads untouched.

## Gate

```
python ops/unclaimed.py --module ov006 --json work/unclaimed-ov006.json
python ops/gen_jumptable_carrier.py --scan      # 66-row plan from the ledger + image
python ops/gen_jumptable_carrier.py --write     # recreate the lane sources
python ops/verify_data_rows.py                  # 66 rows, 42976 B, 0 failures
python ops/verify_data_rows.py --record         # refresh the pinned fixture
python ops/scan_jump_tables.py --module ov006 --unclaimed work/unclaimed-ov006.json
python public_tools/source_units.py --root . --check      # unresolved: 0
python -m unittest ops.test_jumptable_carrier             # 9 tests
```

Regeneration reads the pinned private inputs (`extract/`, `ledger/functions.jsonl`,
`manifest.json`, `tools/mwccarm` and `tools/android-ndk` for the pinned LLVM
objdump); the committed sources and fixture are the record when those inputs are
not present. Verification needs `manifest.json` to carry each module's `bytes`,
`base` and `binary`, because the relocation patcher resolves a Thumb `BL`/`BLX`
mode from the caller's measured image. The `main` rows need no `.s` build path:
their carrier is the `dcd` `asm` body.

`ops/data_rows_expectations.json` pins, per row, the relocation table
(2,098 entries), the image word behind every `R_ARM_ABS32` slot (70 pool words),
the negative control's differing offsets and the section pad length.
`ops/jumptable_carrier_plan.json` pins the lane's enumeration: module, address,
carrier and table extent for every row. The scanner proves the table boundary
from the entries themselves and the verifier proves it again by byte identity;
a wrong split cannot assemble back to the measured bytes.

Source-first screening on a pristine `origin/main` `src/` reports **0 of the 66
addresses already defined**. The lane's rule fragment is
`config/rules.d/jumptable-carrier.json` (three globs: `ov006/arm` p003,
`ov006/thumb` p033, `main/arm` p003); the base `config/source_units.json` is not
edited.

## Source-form rules these rows keep

1. **A data run is emitted as data.** The carrier is chosen by the data width
   and alignment, never by convenience.
2. **A pool word is a relocation, not a constant.** A word that lands inside the
   module image is a `native_fn_`/`native_data_` symbol with its measured addend;
   a word outside the image keeps its measured numeric value (the project's
   established pool-word rule), and a magic constant stays numeric.
3. **A call is a named symbol, never a raw offset**; a Thumb function pointer
   keeps its `+1`.
4. **The measured extent is the whole body.** Code before the data and code
   after it are transcribed; nothing is dropped at the table.
5. **One negative control per row.**
6. **One address-named file per function**, in the carrier's directory.

## Rows

`c` is the mwccarm `dcd` carrier; `s` is the mwasmarm `.hword` carrier. The
last column is the data extent(s) inside the row (`start:length`).

| row | bytes | carrier | data run(s) |
| --- | ---: | --- | --- |
| `main:0x2025578` | 952 | c | 0x202562c:256 |
| `main:0x202654c` | 1348 | c | 0x2026684:256 |
| `ov006:0x21d7478` | 696 | c | 0x21d74cc:16 |
| `ov006:0x21d8414` | 420 | c | 0x21d8480:32 |
| `ov006:0x21d8874` | 5728 | c | 0x21d8894:208 |
| `ov006:0x21db5b4` | 132 | c | 0x21db5cc:48 |
| `ov006:0x21dc3b8` | 920 | c | 0x21dc564:24 |
| `ov006:0x21dcd88` | 612 | c | 0x21dcdc0:36 |
| `ov006:0x21dd57c` | 80 | c | 0x21dd588:20 |
| `ov006:0x21ddfa8` | 476 | c | 0x21ddfc8:20 |
| `ov006:0x21df5a4` | 904 | c | 0x21df694:28 |
| `ov006:0x21dfa24` | 784 | c | 0x21dfa3c:32 |
| `ov006:0x21e00cc` | 904 | c | 0x21e0108:44 |
| `ov006:0x21e0454` | 9704 | c | 0x21e0488:260 |
| `ov006:0x21e674c` | 388 | c | 0x21e67a4:16 |
| `ov006:0x21e72c4` | 172 | c | 0x21e72d8:40 |
| `ov006:0x21e9f14` | 532 | c | 0x21e9f2c:28 |
| `ov006:0x21ea144` | 360 | c | 0x21ea15c:32 |
| `ov006:0x21ea3d4` | 652 | c | 0x21ea3f0:56 |
| `ov006:0x21eadd4` | 500 | c | 0x21eadec:24 |
| `ov006:0x21eafe4` | 392 | c | 0x21eaffc:32 |
| `ov006:0x21eb8e4` | 192 | c | 0x21eb90c:16 |
| `ov006:0x2204ae4` | 212 | c | 0x2204b38:24 |
| `ov006:0x21ebc2c` | 2584 | s | 0x21ec5d0:14 |
| `ov006:0x21eceac` | 188 | s | 0x21ecee8:14 |
| `ov006:0x21ecf8c` | 338 | s | 0x21ecfe0:12;0x21ed044:12 |
| `ov006:0x21ed1c8` | 272 | s | 0x21ed242:22 |
| `ov006:0x21ede50` | 196 | s | 0x21edec6:32 |
| `ov006:0x21edf14` | 152 | s | 0x21edf52:42 |
| `ov006:0x21edfe4` | 376 | s | 0x21ee066:40 |
| `ov006:0x21ee15c` | 464 | s | 0x21ee220:40 |
| `ov006:0x21ee348` | 696 | s | 0x21ee366:16 |
| `ov006:0x21ee600` | 104 | s | 0x21ee616:18 |
| `ov006:0x21ee9a4` | 780 | s | 0x21ee9c2:20 |
| `ov006:0x21eecb0` | 104 | s | 0x21eecc6:18 |
| `ov006:0x21ef564` | 660 | s | 0x21ef614:40 |
| `ov006:0x21eff34` | 180 | s | 0x21eff66:46 |
| `ov006:0x21f0170` | 996 | s | 0x21f01a6:22 |
| `ov006:0x21f3660` | 400 | s | 0x21f3702:8 |
| `ov006:0x21f3a78` | 152 | s | 0x21f3a94:12 |
| `ov006:0x21f3b10` | 724 | s | 0x21f3bb6:12;0x21f3c3a:62;0x21f3cda:34;0x21f3d52:74 |
| `ov006:0x21f5740` | 112 | s | 0x21f575a:16 |
| `ov006:0x21f83c8` | 432 | s | 0x21f8400:16 |
| `ov006:0x21f8b70` | 220 | s | 0x21f8b88:10 |
| `ov006:0x21fa620` | 92 | s | 0x21fa65c:18 |
| `ov006:0x21fa67c` | 260 | s | 0x21fa6a4:18 |
| `ov006:0x21fa7f8` | 392 | s | 0x21fa830:16 |
| `ov006:0x21fac5c` | 266 | s | 0x21fac78:18;0x21facb0:8 |
| `ov006:0x21fad68` | 232 | s | 0x21fad82:18 |
| `ov006:0x21fae50` | 104 | s | 0x21fae6a:22 |
| `ov006:0x21fb5e4` | 460 | s | 0x21fb622:38 |
| `ov006:0x21fcc90` | 292 | s | 0x21fcd44:8 |
| `ov006:0x21fce00` | 324 | s | 0x21fce1a:14 |
| `ov006:0x21fe338` | 168 | s | 0x21fe352:8 |
| `ov006:0x21fe6f8` | 244 | s | 0x21fe716:8;0x21fe738:10 |
| `ov006:0x21fe9b8` | 124 | s | 0x21fe9d4:10 |
| `ov006:0x2200ef4` | 492 | s | 0x2200f0c:30 |
| `ov006:0x2201544` | 196 | s | 0x2201570:8 |
| `ov006:0x2201d08` | 180 | s | 0x2201d6c:12 |
| `ov006:0x2202018` | 660 | s | 0x2202036:70 |
| `ov006:0x22022f0` | 124 | s | 0x2202306:20 |
| `ov006:0x220238c` | 308 | s | 0x22023a4:16 |
| `ov006:0x22024e4` | 352 | s | 0x22024fc:14 |
| `ov006:0x22036ac` | 116 | s | 0x22036d2:16 |
| `ov006:0x22037c0` | 124 | s | 0x22037e6:16 |
| `ov006:0x2203a80` | 276 | s | 0x2203a92:8 |

## Unknowns

Byte identity establishes the code and the data, not their meaning. Every file
states its own unknowns; the recurring ones are the field roles behind each
switch, which consumer owns the reciprocal tables' results, and the callee
contracts of the `native_fn_` targets. The two `main` tables are measured
(contents, bounds, monotonicity) but their producer is not established by the
extent. The `ov006` switch cases are transcribed reachability, not recovered C
control flow.
