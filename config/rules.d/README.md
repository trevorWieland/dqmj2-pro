# Lane rule fragments

Put one JSON file here per lane: `config/rules.d/<lane>.json`. It is a JSON array of source-unit
rule objects with the same shape as an entry in `config/source_units.json:rules`. The loader reads
these files in filename order, merges them ahead of the base rule list, and rejects a glob that is
declared twice.

Do **not** add a lane rule to `config/source_units.json`. That shared array caused four consecutive
conflicts (#185, #187, #190, #191); a lane's own fragment file cannot collide with another lane.

```json
[
 {"glob": "src/verified_assembly/20261113_example/ov006/**", "module": "ov006",
  "compilerFlags": "p003",
  "compilerSha256": "89b2fc16c7f1f29ede1e52bdee5bc8ae4d63fe7e50d8074354dfd92c43d47aca"}
]
```

State `glob`, `module` and `compilerFlags`; add `compilerSha256` or `mode` only when they differ
from the most specific parent rule. See `docs/source-units.md` and
`docs/authoring/2026-11-12-rules-fragments.md`.

The first shipped fragments are `config/rules.d/ov006-sweep2.json` (the ov006
sweep-2 lane's thumb and arm directories),
`config/rules.d/jumptable-carrier.json` (the jump-table carrier lane's ov006
arm/thumb and main arm directories) and `config/rules.d/ov006-sweep3.json` (the
ov006 sweep-3 lane's thumb and arm directories), all 2026-11-12. See
`docs/authoring/2026-11-12-ov006-sweep2.md`,
`docs/authoring/2026-11-12-jumptable-carrier.md` and
`docs/authoring/2026-11-12-ov006-sweep3.md`.

`config/rules.d/ov001-close.json` is the ov001 closing lane
(`src/ov001/p12_ov001_close/**`). It is the only fragment whose `compilerSha256` pin
is forced by an *assembly* difference rather than by flag inheritance: mwccarm 2.0/base
inserts an interworking veneer (`b <label+4>`) at an inline-asm label that a backward
branch targets, which makes 364 of that lane's rows 4-64 bytes longer than the measured
extent; 2.0/sp1p5 assembles the same text without the veneer and all 671 rows are
exact. (A transcribed lane placed under `src/verified_assembly/**` inherits the shared
sp1p5 pin and never meets this; a lane outside that tree inherits its module's base
rule, which for ov001/ov000/main resolves to 2.0/base.) See
`docs/authoring/2026-11-12-ov001-close.md`.
