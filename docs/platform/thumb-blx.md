# Thumb BLX-immediate blocker — resolution

Status: evidence report. Conclusion: the 179 ov006 rows are **not blocked by the compiler**. mwccarm
always emits a Thumb `BL` plus an `R_ARM_THM_CALL` relocation; the image's `BLX` is what the
interworking relocation step produces from that `BL`. Applying the relocation with the ARM-target
rule reproduces the rows byte-exactly. One row is delivered as a demonstration.

## 1. The 24-build matrix

Two real ov006 rows with a single cross-mode call were compiled with every installed mwccarm build
(`-O2 -proc arm946e -interworking -thumb`, ledger profile plus `-thumb`), and the call instruction in
the object was decoded:

* row A `0x02201af8` (20 B) — Thumb call `bl 0x02201270` plus cross-mode call `blx 0x02008430`
* row B `0x021fb384` (24 B) — one cross-mode call `blx 0x02002480`

| build | row A | row B |
| --- | --- | --- |
| 1.2/base | bl + bl | bl |
| 1.2/sp2 | bl + bl | bl |
| 1.2/sp2p3 | bl + bl | bl |
| 1.2/sp3 | bl + bl | bl |
| 1.2/sp4 | bl + bl | bl |
| 2.0/base | bl + bl | bl |
| 2.0/sp1 | bl + bl | bl |
| 2.0/sp1p2 | bl + bl | bl |
| 2.0/sp1p5 | bl + bl | bl |
| 2.0/sp1p6 | bl + bl | bl |
| 2.0/sp1p7 | bl + bl | bl |
| 2.0/sp2 | bl + bl | bl |
| 2.0/sp2p2 | bl + bl | bl |
| 2.0/sp2p3 | bl + bl | bl |
| 2.0/sp2p4 | bl + bl | bl |
| dsi/1.1 | bl + bl | bl |
| dsi/1.1p1 | bl + bl | bl |
| dsi/1.2 | bl + bl | bl |
| dsi/1.2p1 | bl + bl | bl |
| dsi/1.2p2 | bl + bl | bl |
| dsi/1.3 | bl + bl | bl |
| dsi/1.3p1 | bl + bl | bl |
| dsi/1.6sp1 | bl + bl | bl |
| dsi/1.6sp2 | bl + bl | bl |

No build emits an immediate `BLX` (halfword 2 in the `0xE8xx` range); every cross-mode call is a
`BL` (`0xF8xx`) with `R_ARM_THM_CALL`. Builds do not differ on this point.

## 2. Source forms on 2.0/base

All forms were compiled and the object call encoding inspected. "BL" means a Thumb BL with a
relocation; "BLX reg" means an indirect `blx rN`.

| form | result |
| --- | --- |
| plain `extern void f(void);` call | BL |
| `__attribute__((noinline))` on the declaration | BL |
| `__attribute__((arm))` on the declaration | BL |
| `__attribute__((interworking))` on the declaration | BL |
| `#pragma arm` before the declaration | BL |
| `#pragma arm` before a locally defined helper, called from Thumb | BL (pragma ignored for mode) |
| `__declspec(arm)` / `__declspec(noinline)` | compile error |
| constant ARM function pointer, called | BLX reg (indirect; does not reproduce the image) |
| `__asm { blx symbol }` | compiles, but assembles to **BL** (`0xF8xx`/`0xFCxx`) with `R_ARM_THM_CALL` |
| `__asm { blx 0x02008430 }` / `blx #0x02008430` / `blx.w 0x...` / `bl 0x...` | `illegal operand` |
| `__asm { .hword ... }` / `.short` / `.word` | `illegal operand` (no raw data in inline asm) |
| `__asm { blx r0 }` | BLX reg (indirect; wrong encoding) |

So no source form forces an immediate `BLX`; the compiler and its integrated assembler both leave
the BL→BLX decision to relocation processing.

## 3. Decisive finding: it is a relocation rule, not a compiler limit

Row `0x02201af8` compiles from plain C to 20 bytes with two `R_ARM_THM_CALL` relocations
(`0x02201270` Thumb, `0x02008430` ARM). Applying the second relocation with the **ARM-target rule**
(encode `BLX` immediate instead of `BL`) yields:

```
object + mode-aware relocations : 08b54088082804d10920fff7b5fb06f694ec08bd
image (ov006 @ 0x02201af8)      : 08b54088082804d10920fff7b5fb06f694ec08bd
```

Full-extent match, 20/20 bytes. Negative control (condition `8` → `9`) fails at object offset 4.
The same rule was already used to author/maintain Thumb packets in `work/author-p1/p1.py`
(`kind == 10`: BL when the target symbol is Thumb, BLX when the target symbol is ARM).

This means the 179 rows should be re-screened with the mode-aware relocation application. The
blocker is in whichever acceptance/build step currently expands `R_ARM_THM_CALL` as a plain `BL`,
not in mwccarm and not in the row sources.

## 4. Recommended workaround and packet format

**Primary (no assembly, packet format unchanged):** make the `R_ARM_THM_CALL` expansion in the
acceptance/build path mode-aware — resolve the target symbol, and if its recorded mode is `arm`
encode the `BLX` immediate form (clear bit 12 of the second halfword, use the `imm10L` layout),
otherwise keep `BL`. Re-run the 179-row screen; sources stay ordinary C, negative controls unchanged.
If the acceptance path is the private `public_tools/repo_build.py` relocation expander, this is a
single-function change plus a regression test on row `0x02201af8`.

**Fallback (only if the relocation path cannot change):** justified assembly for the affected call
site is *not* available through inline asm in this compiler (`blx` with an immediate operand is
rejected, and inline asm assembles a symbol `blx` as `BL` anyway). The only assembly route would be a
per-row `.s` implementation of the whole function assembled with the project assembler, recorded as
"assembly justified by a measured toolchain/linker limitation" with the usual exact-bytes and
negative control evidence. This is heavier and appears unnecessary given the primary finding; it
should not be used while the relocation rule is fixable.

## 5. Demonstration row

`src/ov006/p1n_ov006_blx/native_main_02201af8.c`:

* `0x02201af8`, 20 bytes, exact with the mode-aware relocation application (2 relocation rows),
* negative control (`== 8` → `== 9`) fails at offset 4,
* profile `-O2 -proc arm946e -interworking -thumb`.

## 6. Limits of this report

* The matrix covers the installed builds only (24); an uninstalled build could behave differently.
* `mwasmarm.exe` rejected `blx #0x02008430` for the tested processor options; the repo's exact
  assembler invocation for `.s` inputs was not identified within the box, so the per-row assembly
  fallback is specified but not demonstrated.
* Which acceptance step currently expands `R_ARM_THM_CALL` was not traced; the row-level proof shows
  the mechanism, and the re-screen is the next step.
