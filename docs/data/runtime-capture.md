# Runtime RAM capture

Status: specification plus tooling. **No runtime was executed and no real capture
was performed.** The rehearsal in this document uses a generated buffer.

## Why this exists

`docs/data/unbacked-data.md` proves that some data only exists after the program has
run:

- `species_roster` at **`0x021c4bf8`**, 24-byte records, inside **main BSS**
  (`0x020e3300`–`0x021d7240`, 999,232 bytes, recorded as `expectedBssBytes` in
  `manifest.json` and as the `.bss` span in the delinks files);
- the script VM's **output text block** at **`0x020fb264`** (`native_data_020fb264`),
  likewise runtime state. `docs/scripts/vm.md` §3 proves it: the write handlers
  advance a byte cursor stored at `native_data_020fb264 + 0x80`, and the text itself
  is a `u16`-indexed array at `native_data_020fae64` addressed by that cursor.

BSS is zero-filled at load and never file-backed, so no ROM extraction can produce
these bytes. A RAM dump taken from a running instance is the only source, and it
has to carry provenance or it is unusable: bytes from an unknown build, at an
unknown point in the game, prove nothing.

## 1. What is available locally for runtime execution

**Nothing that this deliverable may use.** Findings:

- no emulator is bundled or installed in the checkout; there is no emulator
  directory, no wrapper script, and no ROM-running harness anywhere in `tools/`,
  `ops/` or the tracked tree;
- `docs/2026-10-27-toolchain.md` records melonDS 1.1 as "an upstream candidate, not
  an installed or validated tool here. No emulator instance was launched." The
  project has historically avoided melonDS sessions, so it is not a permitted
  capture tool for this lane;
- `ports/runtime/` is a source-mapping area (generated C ports), not an emulator.

Therefore this lane delivers **specification and tooling only**. Capturing is a
human, offline, muted action with a permitted tool, recorded in the spec; nothing
here automates or performs it.

### Permitted tools (for a human with the ROM and a host)

Either of these, on an isolated machine, muted, with a copy of the save:

| tool | how to get a memory dump | notes |
| --- | --- | --- |
| DeSmuME 0.9.11+ | Debugger → Tools → Dump Memory; pick address + size | writes a raw little-endian `.bin` |
| no$gba 2.8 | Utility → Dump memory | raw `.bin`, address range configurable |

Both are offline reference tools; neither is installed here and neither is run by
this deliverable. Do not attach a debugger, do not enable audio, and do not run
with the original save — use a copy.

## 2. What state to capture

| target | address | bytes | state the game must be in |
| --- | --- | --- | --- |
| roster | `0x021c4bf8` | **360** (15 records × 24 B) | roster **populated**: the monster farm or party screen open with all 15 slots filled, so no record is a zero placeholder |
| VM output text block | `0x020fb264` | 1024 (block + cursor at `+0x80`; the printed text array sits at `0x020fae64`) | **mid-scene**: a scene that has printed text, not the title screen and not a paused menu |

Dump the whole main-RAM window rather than the two ranges. The tool requires the
dump to **cover the module window from its base** (`0x02000000`–`0x021d7240`:
`930,560` image bytes plus `999,232` BSS bytes, from `manifest.json`), and a dump
may be larger than that — a real debugger dump is usually the full 4 MiB
`0x02000000`–`0x02400000`, which is accepted and sliced from. What is refused is a
dump that starts after the module base or ends before the module end, because every
captured byte would silently shift.

Record while dumping, and put all of it in the spec:

- `buildSha256`: SHA-256 of the **exact ROM image** used (copy it from
  `manifest.json` `rom.sha256` if you used `inputs/game.nds` — the tool refuses a
  mismatch);
- `tool`: emulator name and version, plus the menu path used;
- `capturePoint`: one sentence describing the in-game state;
- `timestampUtc`: when the dump was taken.

## 3. Running the capture tool

```bash
# validate only — no output written
python ops/ram_capture.py --spec captures/ram-roster-20261110.json --check

# slice, hash, write extract/ram/, emit the manifest fragment
python ops/ram_capture.py --spec captures/ram-roster-20261110.json

# additionally write a manifest copy with the new module entries merged in
python ops/ram_capture.py --spec captures/ram-roster-20261110.json \
    --apply-manifest build/ram-capture/manifest-with-ram.json
```

Spec:

```json
{
  "dump": "work/ram/roster.bin",
  "dumpBase": "0x02000000",
  "module": "main",
  "provenance": {
    "buildSha256": "674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6",
    "tool": "DeSmuME 0.9.11 (Debugger > Tools > Dump Memory)",
    "capturePoint": "monster farm open, 15 roster slots filled",
    "timestampUtc": "2026-11-10T21:00:00Z"
  },
  "captures": [
    {"name": "ram-roster", "address": "0x021c4bf8", "bytes": 360},
    {"name": "ram-scriptvm", "address": "0x020fb264", "bytes": 4096}
  ]
}
```

The tool refuses, with exit `1` and nothing written, when:

- a provenance field is missing, or `buildSha256` differs from `manifest.json`
  `rom.sha256` (bytes from another build are not evidence);
- the dump does not cover the module window the manifest claims (`main` =
  `0x02000000`–`0x021d7240`, image plus `expectedBssBytes`): a dump that starts late
  or ends early silently shifts or truncates every byte. A dump **larger** than the
  window is accepted;
- `--apply-manifest` targets `manifest.json` itself, a file inside the private
  trees (`ledger/`, `extract/`, `inputs/`, `deps/`, `tools/`, `config/`, `src/`), a
  tracked file, or any path outside the checkout — a worktree's `ledger/` is a
  junction to the parent repository, so an apparently local copy can be the real
  ledger. Only a copy under `build/` is writable;
- a capture range leaves the module, leaves the dump, or has a non-positive size.

Each accepted capture is written to `extract/ram/<name>_<address>.bin` and gets a
manifest module entry (`name`, `base`, `loadAddressBase`, `binary`, `bytes`,
`sha256`, `kind: runtime-capture`, and the full provenance including the dump hash).
`public_tools/data_dump.py` then treats it as an ordinary module: point the data
dictionary table's `module` at the capture name.

## 4. How to validate a real capture

Mechanical validation is the tool's job; semantic validation is the point of the
capture and has to be done by eye against the dump:

1. `--check` passes (provenance, ranges, sizes).
2. **Roster sanity** — heuristics, not proof. The slice must be 15 records × 24 B
   with:
   - `species` (`s16` at `+10`) inside the set the matched readers compare against
     — `139, 176, 188, 254, 350, 425, 426` appear in `native_main_0206db00`, so a
     *plausible* roster contains several of them. This is a provenance check on the
     game state, not a layout proof;
   - `count` (`u8` at `+1`) and `first` (`s8` at `+2`) **small values (1–4)**. This
     is an **unproven sanity heuristic**: the fields are proven to exist at those
     offsets, but no matched code constrains their range, so a larger value is not
     by itself evidence of a bad capture;
   - no record that is entirely `0x00` or entirely `0xFF` — an empty slot or
     uninitialised memory rather than a populated roster. Also a heuristic.
3. **VM text block sanity** — supported by `docs/scripts/vm.md` §3, which proves
   the byte cursor lives at `native_data_020fb264 + 0x80`. A plausible capture has
   that cursor byte well below the 1024-byte block (a text run of normal length),
   the block is not uniform fill, and the `u16` array at `0x020fae64` addressed by
   the cursor contains text values rather than pointers. The block is **not** a
   command stream: do not validate it as opcodes.
4. Record the observed values in the capture's commit message or PR description —
   the bytes are private, the observation is the evidence.

## 5. Rehearsal performed by this deliverable

No emulator, no ROM execution. A synthetic dump was generated
(`work/p2/make_synthetic_ram.py`, scratch, gitignored): a 1,929,792-byte buffer
covering `0x02000000`–`0x021d7240` with a deterministic pattern, 15 roster records
filled at `0x021c4bf8` (species `139, 176, 188, 254, 350, 425, 426, …`) and a
4,096-byte pattern block at `0x020fb264`. A second 4 MiB buffer covering the full
`0x02000000`–`0x02400000` window was generated to prove that a larger-than-module
dump is accepted and sliced.

Proved with it:

| check | result |
| --- | --- |
| `--check` validation and slicing | passes; `ram-roster` 360 B at `0x021c4bf8`, `ram-scriptvm` 4096 B at `0x020fb264` |
| slice + hash + fragment emission | `extract/ram/*.bin` written, manifest fragment with two module entries |
| `data_dump.dumpability()` on the merged manifest | `dumpable` |
| `data_dump.read_table()` from the captured module | 15 rows, species column `139, 176, 188, 254, 350, 425, 426, …` |
| full 4 MiB window dump | accepted, sliced from |
| truncated dump (4 KiB) | refused, exit 1, "dump ends … before the module end" |
| capture past the module end | refused, exit 1 |
| wrong build hash | refused, exit 1, explicit hash mismatch |
| `--apply-manifest manifest.json` | refused, exit 1 |
| `--apply-manifest ledger/modules.json` (junction to the parent repo) | refused, exit 1, "outside the checkout" |
| `--apply-manifest ops/ram_capture.py` (tracked) | refused, exit 1, "tracked file" |
| `--apply-manifest build/.../copy.json` | accepted |

**No real capture was performed, and nothing here claims the roster contents are
known.** The synthetic bytes exist only to exercise the tool's slicing, verification
and manifest emission.

## 6. Out of scope

- Installing or running an emulator, or automating gameplay, from this repository.
- Audio, graphics or save-file extraction; anything that would need the original
  save rather than a copy.
- Proving the roster **record count** is 15 (that follows from the 360-byte block
  the parent lane specified; a real capture is what confirms it).
- The `native_data_020fb264` command block's internal layout — this lane captures
  bytes, it does not decode the VM.
- Any change to `manifest.json`, `ledger/` or `public/accepted-functions.json`: the
  tool writes a fragment and an optional manifest **copy**; promoting a capture to
  the real manifest is an integrator decision.
