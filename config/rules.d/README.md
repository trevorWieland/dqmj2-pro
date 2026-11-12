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

`config/rules.d/ov006-sweep2.json` is the first shipped fragment (the ov006
sweep-2 lane's thumb and arm directories, 2026-11-12).
