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

These statements are scoped to the **text VM family** documented above (the dispatcher
`native_main_02047428` and its three handlers). They do **not** describe the interpreted SCR
script system as a whole, which has its own, separately documented dispatcher (§7).

* **Terminate:** proven for this family, two forms — `0x00` ends a walk, `0xe3 0x1b` ends a
  block (§4).
* **Call / return:** *unknown for this family*. No matched function in it maintains a return
  address, call depth or jump table.
* **Branching:** *unknown for this family*. The dispatcher computes no jump target; the walk
  in §4 is strictly linear.
* **SYS / system-service nodes:** **not part of this family.** The interpreted SCR system's SYS
  dispatch is a separate, already-measured mechanism — the ARM9 dispatcher table at
  `0x0205A68C` with 358 slots and a default block at `0x0205BCF0` (§7). This document makes no
  claim about it beyond citing the inventory.

## 6. Script image container — documented by the existing inventory

The SCR container is **already documented in the repository**; it is not an open question and
this document must not imply otherwise. See
[`docs/2026-10-29-interpreted-script-inventory.md`](../2026-10-29-interpreted-script-inventory.md)
and `manifest.json` → `interpretedCoverage`:

| measured item | value |
| --- | --- |
| Known member-zero script archives | 341 |
| FPK member-table identities | 1,132 |
| Distinct decoded script images | 297 |
| Unique code-container bytes | 14,237,108 |
| Reached opaque SYS nodes | 121,682 |
| Uncovered container bytes | 104,232 |
| Reconstructed ordinary script-source units | 0 |

Decoded layout, from that inventory: **SCR magic, a 4096-byte table of 1024 signed entry
offsets, then code starting at member offset 4100**. The archives themselves are FPK files
(`FPK\x00` magic) whose members decode to those SCR images; duplicate member images reduce
341 archives to 297 distinct images. `extract/files/*.e` are those archives — for example
`d145.e` is an FPK container, and its decoded member is the 10,724-byte code interval named in
the inventory.

What this document adds is the *text VM* model (§1-§4), which is a different mechanism from the
SCR bytecode. What it does not add, and never claimed, is a second container finding.

## 7. Relationship to the interpreted SCR inventory

The existing inventory and this document measure different things, and the difference is worth
stating plainly:

| | interpreted SCR inventory | this document / `scr_disasm.py` |
| --- | --- | --- |
| Subject | SCR bytecode in FPK members (297 images, 14,237,108 bytes) | the text VM family (`native_main_02047428` handlers) |
| Container | documented: SCR magic, 4096-byte entry table, code at 4100 | not restated; cited only |
| SYS dispatch | measured: table `0x0205A68C`, 358 slots, default `0x0205BCF0`, 121,682 opaque nodes | out of scope |
| Opcode coverage | partial CFG over reached records, `completeControlFlowCoverageCertified: false` | 47 opcodes of one dispatcher family, parsed from matched source |
| Output | CFG evidence artifacts (private, generated) | human-readable listing of a byte window |

**What `scr_disasm.py` does not cover:** it does not parse FPK archives, does not decode
members, does not read the 4096-byte SCR entry table, and does not decode SCR opcodes or SYS
records. Pointing it at `extract/files/*.e` is refused with that explanation. Use the pinned
FPK/ASH reader and the inventory's CFG tooling for those.

## 8. What the tool proves today

