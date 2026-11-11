# ops/

Private-side operating tools. Everything here may read the private inputs
(`ledger/`, `manifest.json`, `extract/`, `inputs/`), so these scripts are not part
of `public_tools/` and are not run by CI's public build.

## `symbol_map.py` — generated symbol map (deliverable D1)

Emits the canonical address → symbol map from the address ledger.

```bash
python ops/symbol_map.py --root <private-checkout>            # write the map
python ops/symbol_map.py --root <private-checkout> --check    # verify naming only
```

Outputs (generated, **never committed**; default `build/symbol-map/`):

| file | contents |
| --- | --- |
| `symbols.txt` | one line per symbol: `<address> <size> <module> <mode> <name>` |
| `symbols.json` | the same rows plus `processor`, `source`, `nameSource`, `accepted` |

Rows are sorted by module then numeric address, so the output depends only on the
inputs. It reads `ledger/functions.jsonl` (one row per measured function) and
`manifest.json` (the module inventory); `--root` defaults to the current directory.

### Name resolution

The ledger symbol is used when it is a real name. When it is the
`func_XXXXXXXX` placeholder the name comes from, in order:

| `nameSource` | rule |
| --- | --- |
| `ledger` | the ledger already carries a real symbol |
| `source` | a function definition in the row's `sourceUnit` whose identifier contains the address, the only definition in that file, or the file stem when it encodes the address |
| `dependency` | another ledger row's relocation targets this address with a real symbol name (call sites name their callee) |
| `definition-order` | the row's file has exactly as many unclaimed definitions as unclaimed rows: paired in address order with definition order |
| `unresolved` | none of the above — kept at the address-derived ledger symbol |

Rows that stay unresolved are emitted with an **address-derived name** (the ledger's
`func_XXXXXXXX`, or the module-qualified `func_<module>_XXXXXXXX` for arm7 rows that
have no source at all) and `nameSource: "address-fallback"`, so a consumer can always
see which names were not resolved from evidence.

`--check` verifies naming only and writes nothing. It exits non-zero when an accepted
row (`states.functionMatched`) is unresolved. `--allow-unresolved [N]` relaxes that to
a ceiling: with the flag alone `N` is the documented baseline
(`UNRESOLVED_BASELINE = 151`), so CI gates on "no new unresolved rows" instead of
absolute zero; `--allow-unresolved 0` restores the strict check and a larger `N`
lowers the bar further.

Measured on the current private ledger: 16,073 rows over 18 modules, 11,660
accepted, with 9,485 names from the ledger, 5,102 from source definitions, 193 from
relocation evidence, 85 from definition order, and 1,208 rows on
`address-fallback`, of which 151 are accepted.

The 151 accepted residual is deliberate and must not be papered over with invented
names: each is a main-module function whose source defines a semantic name that
neither carries the address nor appears as any taken relocation target, and whose
file does not have a row-count to definition-count match that would allow an
unambiguous pairing. The only evidence that could name them — the original object
symbol tables (`row['object']`) and the match reports (`evidence/matches/*.json`) —
was pruned from the private tree, so recovering them needs either a re-run of the
link that produced them or a decision to accept the address-derived names. Until
then `--check --allow-unresolved` passes at the baseline and fails if the count
grows. The text map is stable across runs.
