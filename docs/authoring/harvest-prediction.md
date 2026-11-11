# Harvest prediction from disassembly — ov006 40-80 B experiment

Status: experiment report. Question: can we predict, from disassembly alone, whether a Thumb family
will be harvestable by hand (one row authored, template applied to the rest) before authoring
anything? The display family harvested 9/9; the channel-state family reached exact size and matched
0/6. This note records the features measured, two predictions, the outcomes, and the rule the
outcomes support.

Tools used: `ops/screen_candidates.py` (ov006) and `ops/check_duplicate.py` before selecting rows;
the family census and per-row features were computed from the ledger plus Capstone disassembly.

## Families measured (no authoring)

Ten ov006 families in the 40-80 B band, clustered by the first eight mnemonics. Features:
`calls` = bl/blx count; `reload` = a load from `[pc]` or `[sp]` after the last call; `saved` =
callee-saved registers in the prologue push (r4-r11); `cb` = chained callback (a code pointer
literal passed to a call, as in the channel-state tail chain); `stack` = stores to `[sp]` before a
call; `chain` = load-through-pointer-from-a-global record chain.

| # | family (mnemonic prefix) | rows | B | calls | reload | saved | cb | stack | chain | score (of 6) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | push sub adds ldr ldr ldr ldr ldr (channel-state) | 6 | 424 | 2 | 0 | 1 | 0 | 3 | 1 | 3 |
| 2 | push bl cmp beq cmp beq pop movs | 5 | 288 | 6 | 0 | 0 | 0 | 0 | 0 | 5 |
| 3 | ldr ldrh movs lsls ands asrs beq movs | 4 | 212 | 0 | 0 | 0 | 0 | 0 | 1 | 5 |
| 4 | push ldr ldr bl ldr movs ldrh movs (display remnant) | 4 | 304 | 1 | 1 | 0 | 0 | 0 | 1 | 4 |
| 5 | push sub adds ldr movs ldr add ldr | 3 | 200 | 4 | 0 | 1 | 0 | 1 | 0 | 4 |
| 6 | push sub ldr ldr ldr adds ldrb str | 3 | 144 | 1 | 0 | 0 | 0 | 2 | 1 | 4 |
| 7 | push cmp bne ldr movs ldr lsls ands | 2 | 156 | 0 | 0 | 1 | 0 | 0 | 0 | 6 |
| 8 | push ldr movs ldr ldr bl ldr ldr | 2 | 80 | 3 | 0 | 0 | 0 | 0 | 1 | 4 |
| 9 | push lsls ldr ldr bl movs movs bl | 2 | 116 | 5 | 0 | 1 | 0 | 0 | 1 | 4 |
| 10 | push sub adds ldr ldr adds adds ldr | 2 | 160 | 2 | 0 | 1 | 0 | 3 | 1 | 3 |

## Predictions

- **P1: family 7** (`push cmp bne ldr movs ldr lsls ands`, members 0x2203908, 0x2203954, 156 B) —
  highest score 6/6: no calls, no reload, one saved register, no callback, no stack arguments,
  no record chain. Predicted harvestable.
- **P2: family 3** (`ldr ldrh movs lsls ands asrs beq movs`, members 0x2203EBC, 0x2203EEC, 0x2203F1C,
  0x220410C, 212 B) — score 5/6: no calls, no saved registers, no stack arguments. Predicted
  harvestable.

## Outcomes

- **P1 — actual 0/2.** Both members collapsed to 44/76 and 48/80 bytes: the measurement selects one
  of two register banks with a branch (`ldr r0,=0x04001000` vs `movs r0,#1; lsls r0,#0x1a`), and the
  C form `if (select == 1) reg = ...; else reg = ...` compiled the selection away into a single
  computed address. The feature set did not see the branch-merged pointer select as a risk.
- **P2 — actual 0/4.** All four compile to the exact native size (48/48 and 68/68), but the
  comparison idiom differs: the measurement emits `ands r1,r0; cmp r0,r1; bne` for a mask-equality
  test, while C `(field & value) == value` emits `ands r1,r0; bics r1,r0; bne` (mask-clearing idiom).
  A volatile local forces the literal compare but overshoots to 72/48. The 68 B member additionally
  differs on a byte bit-test (`tst` vs `lsls/lsrs` shift extract). The features measured allocation,
  not expression-idiom determinism.

Both predictions were wrong, and both wrong for the same reason: the feature set described *shape*
(calls, registers, stack) but not whether each C expression maps to one fixed instruction idiom.

## Prediction rule (revised)

A family is predicted harvestable from disassembly only if **all** of the following hold:

1. `calls == 0`, or every call is followed by no reload and no branch on its result;
2. `saved <= 1`;
3. `stack == 0`;
4. `chain == 0` (no record chain: global -> record -> field);
5. **no branch-merged pointer/literal select** — the row does not choose between two address
   constants in an if/else that feeds a dereference;
6. **no mask-equality comparison** — the row does not test `(x & m) == m` or `(x & m) == 0`
   (compiler may pick `bics`/`tst` instead of `ands; cmp`);
7. **no byte bit-test** that the measurement implements with a shift-extract (a plain `& 1` may
   become `tst`).

Rule of thumb: harvestable families are straight-line register/MMIO writes with at most one call
and no conditional data selection. Conditions 5-7 are the ones that cost P1 and P2; they are visible
in disassembly as a branch that selects an address, an `ands`/`cmp` pair where one operand is a
constant mask, or `lsls`/`lsrs` around a byte load.

## What this says for capacity planning

- The display family (9/9) satisfies the whole rule: straight-line stores to fixed MMIO addresses,
  one call, no conditional selection, no mask-equality.
- Channel-state (0/6) fails rule 4 and 5; P1 fails rule 5; P2 fails rules 6 and 7 despite scoring
  highest on the old features.
- Practical filter: take a candidate family, check rules 1-4 mechanically, then read only the
  branch bodies for rules 5-7. Families that pass all seven have been the only ones that harvested;
  families that pass 1-4 but fail 5-7 should go to the permuter lane directly, not to authoring.

## Reproduction

`work/author-p1/p1t_features.py` prints the feature table from the ledger and image.
`ops/screen_candidates.py --module ov006 --root . --max-bytes 80` produces the ready-row census.
`ops/check_duplicate.py --root . --address ...` was run on the six attempted rows (all clear; one
address is only mentioned as a declaration in another unit, which `--allow-mentions` accepts).
