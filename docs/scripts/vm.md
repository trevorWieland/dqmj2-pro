# Script / command VM

Status: **first increment**. What follows is only what matched native code proves; the
sections marked *unknown* are the parts the recovered sources do not constrain. This lane is
almost entirely unrecovered (0.30%), so the model is thin by construction rather than by
choice.

## 1. The entry point and dispatch — proven

`src/runtime/parallel_wave20261104/main-command-middle/first/02047428.c` (function
`native_main_02047428`) is a matched command dispatcher:

```c
u8 native_main_02047428(const u8 *input)
{
    int opcode = *input;
    u8 used = 1;
    ...
    ++used;
    switch (opcode) { case 0x21: ... }
```

Proven by that body:

* **The stream is addressed by a byte pointer**; the opcode is the first byte at the pointer
  (`opcode = *input`).
* **Every command consumes at least two bytes.** `used` starts at 1 and is incremented before
  the dispatch, i.e. the base command size is 2, not 1.
* **Dispatch is a plain C `switch` over the opcode byte**, not a function-pointer table: the
  matched function contains 47 `case` arms.

## 2. Opcode table — proven (47 opcodes, 3 handler families)

The arms call three handlers, each of which contributes to `used` through its return value:

| family | handler | call shape | role (proven) |
| --- | --- | --- | --- |
| `walk` | `native_main_02047ac0` | `walk(0)`, `walk(32)` | walks the text block, see §4 |
| `text` | `native_main_02047b90` | `text(target, a, b, c)` | writes a run into the text block |
| `alt` | `native_main_02047bfc` | `alt(target, a, b, c)` | same shape, different source buffer |

The opcode bytes, and the exact `(a, b, c)` triples, are read out of the matched source by
`public_tools/scr_disasm.py --opcodes` (it parses the `case` arms at run time, so the table
cannot drift). Families and parameters, proven:

* `0x28..0x2d`, `0x8e..0x9d` → `text`, with `a ∈ {0,1,2}`, `b ∈ {0,1}`, `c ∈ {0..3, 255}`.
* `0x38..0x3d`, `0x9e..0xad` → `alt`, with the same parameter shape.
* `0x22` / `0x24` → `walk(0)` / `walk(32)`.
* `0x21` → no statement (a no-op arm).

The `(a, b, c)` triples look like a grid of three small selectors, but **what each selector
means is unknown**: the handlers never interpret them; they forward them to
`native_fn_02047d50` / `native_fn_02047c68`, whose bodies are not recovered.

## 3. The text block, cursor and produce length — proven

Both write handlers (`src/runtime/runtime08/native_main_02047b90.c` and
`native_main_02047bfc.c`) follow the same five steps:

1. `native_fn_02008c14(0, native_data_020fad60, 0x80)` (or `native_data_020facdc`) — clear a
   0x80-byte scratch buffer.
2. `native_fn_02047d50(a, b, c)` / `native_fn_02047c68(a, b, c)` — build one produced string.
3. `native_fn_02021294(target, temp) ` — copy it to `target`.
4. `native_data_020fb264[0x80] += native_fn_02021258(temp)` — **advance a cursor stored at
   offset `0x80` of `native_data_020fb264` by the produced length**.
5. `return 0`.

So the VM's output is a text block whose byte cursor lives at `native_data_020fb264 + 0x80`,
and `native_fn_02021258` is the produced-length function. `target` is
`native_data_020fae64 + native_data_020fb264[0x80]` (computed once in `native_main_02047428`),
i.e. a `u16`-indexed array at `native_data_020fae64` addressed by that cursor.

**Value/stack model: unknown.** No matched function pushes, pops, or reads a stack; the
evidence is a write cursor, not an operand stack.

## 4. Linear walk, escapes and terminators — proven

`src/runtime/parallel_wave20261104/main-command-middle/third/02047ac0.c`
(`native_main_02047ac0(position)`) walks the same block:

* A command whose first byte is `0x00` **ends the walk** (`if (!*command) break;`).
* `0xe3 0x1b` **ends the block** (`if (*command == 0xe3 && command[1] == 0x1b) break;`).
* `0xe3 0x1c xx` skips `native_fn_02047018(command[2])` bytes.
* `0xe3 0x15` skips `native_fn_02046fc8()` bytes.
* Any other byte advances by `native_fn_02046e68(command)`, **the per-command length
  function**.

`native_fn_02046e68`'s body is not recovered, so **the operand widths of the general command
encoding are unknown**. This is the single measurement that would turn the listing from
"opcode bytes" into "instructions": until it is matched, `scr_disasm.py` consumes exactly one
byte per command and says so.

## 5. Control flow — SYS / call / terminate

* **Terminate:** proven, two forms — `0x00` ends a walk, `0xe3 0x1b` ends a block (§4).
* **Call / return:** *unknown*. No matched function maintains a return address, call depth or
  jump table.
* **SYS (system service) nodes:** *unknown*. Nothing matched names or dispatches a SYS opcode.
* **Branching:** *unknown*. The dispatcher has no jump target computation; the walk in §4 is
  strictly linear.

## 6. Script image container — unknown

The extract's `extract/files/*.m` images are `FPK` archives (`46 50 4b 00` magic, then
file-name entries such as `k01e010a.nsbmd`), i.e. model/texture packs, **not** the command
stream. The command block the VM reads (`native_data_020fb264`) is assembled in RAM, so no
ROM image is known to contain a ready-made stream. The 297-image / 14.2 MB script body is
therefore **not yet located** by this work; that is a container-format question, not an
opcode question.

## 7. What the tool proves today

`public_tools/scr_disasm.py`:

* `--opcodes` prints the 47-opcode table parsed from the matched dispatcher.
* `--image … --offset … --length …` decodes a window: known opcodes as their proven
  mnemonic and `(a,b,c)`, `0x00` as `.end`, `0xe3 0x1b` as `.block_end`, `0xe3 0x1c xx` as
  `.escape_skip`, and **anything else as `.byte … ; unknown opcode`**, with a coverage line
  (bytes read / decoded / undecoded).
* `--streams` / `--scan` list the longest known-opcode runs in an image so a real stream can
  be found if one exists.

Tested on two real images from the private extract (`extract/files/ActTbl.bin`,
`extract/files/AIActionTbl.bin`): no terminator-ended run of four or more known opcodes was
found, and window decodes are dominated by unknown bytes (e.g. `ActTbl.bin` offset 0: 4 bytes
read, 1 decoded as `.end`, 3 unknown → 25%). That is the honest state: the opcode table is
proven, the container that stores streams is not.
