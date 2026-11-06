# ARM9 shared arithmetic entry, 2026-10-29

`0x02025F2C` is an independently callable ARM entry inside the configured 448-byte parent at `0x02025F1C`. It has its own identical seven-word push frame and distinct selection/sign setup before joining `0x02025F3C`. This evidence qualifies an alternate native entry; it grants zero reconstructed C or assembly bytes and does not double-count the parent's executable coverage.

The measured main image SHA-256 is `ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f`. The parent span hashes to `b60335594ae240c00bda300b86a06eaf9eb871382b5ab9dc2b0a6810971df060`. The configured parent is `func_02025f1c kind:function(arm,size=0x1c0)`; the current alternate identity is `.L_02025f2c kind:label(arm)`.

## Measured entry and ABI

Both prologues push R4–R7, R11, R12, and LR, taking exactly 28 stack bytes. The first entry copies R1 to R4 and sets bit zero. The alternate XORs R1/R3 into R4 and clears bit zero through arithmetic-right/left shifts. Every fixture independently verifies those entry instructions, the five-address prefix through the shared join, its own saved stack words, and the selection word at the join.

Numerator words are R0 low/R1 high; denominator words are R2 low/R3 high. Results use R0 low/R1 high. The first entry produces signed remainder; the alternate produces signed quotient. R4–R14, including SP and LR, are preserved. R2/R3 and NZCV are not assigned a preservation contract. Both ARM and Thumb returns work.

Three exceptional behaviors are measured explicitly:

- Denominator zero returns the original numerator unchanged at either entry, without a fault or external call.
- `(-2^63)/(-1)` wraps to `-2^63`; the remainder is zero.
- The signed32 fast path makes `(-2^31)/(-1)` produce `-2^31`, rather than mathematical `+2^31`; its remainder is zero. The path calls native `0x02026144`, then sign-extends its word result at `0x02025F74`.

These are target-runtime observations. They are not claims about defined C division-by-zero or overflow semantics.

## References and bounded execution

Exact direct native branches corroborate the alternate entry:

| Source module/function | Branch | Target |
| --- | --- | --- |
| main `0x02002210` | `0x020022F0` | `0x02025F2C` |
| main `0x0200FE50` | `0x0200FEA0` | `0x02025F1C` |
| main `0x0200FE50` | `0x0200FEC0` | `0x02025F2C` |
| ov000 `0x021E035C` | `0x021E03E0` | `0x02025F2C` |

The reproducible suite uses 612 operand pairs, including signed32/signed64 boundaries, all sign combinations, denominator zero, overflow, and deterministic random32/random64 values. Across both entries, both return modes, and two incoming IRQ/FIQ-mask settings, all 4,896 fresh native machines actually return. The maximum observed path is 1,129 instructions under a 20,000-instruction limit. All memory writes remain in the measured 28-byte saved frame; other control bits and preserved registers agree with the independent model.

Small operands execute the separately configured 524-byte native helper at `0x02026144`. Larger operands execute the parent's shared arithmetic body. Those original bytes are analysis scaffolding with zero source credit; no synthetic callee implementation is used.

## Reproduction and provenance limits

Run `python verify_main_20261029_div64_entry.py`. The report is `evidence/entrypoints/main-20261029-div64-entry.json`, including exact prologue bytes/hashes, input/module identity, qualified branch references, every fixture result and digest, native helper hash, and bounded local reference-search results.

Repository-local tools/dependencies and pinned compiler-archive members were searched for an original ARM runtime assembly reference. The available host MSL DLL names do not establish ARM source provenance. No original vendor symbol name or verified-original assembly source is established by this evidence. The integrator owns alternate-entry ledger/linker adoption and any future source recovery.
