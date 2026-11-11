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
| `unresolved` | none of the above — the placeholder is kept |

`--check` exits non-zero when an accepted row (`states.functionMatched`) is still
`unresolved`, and prints the count plus the first twenty rows. It does not write the
map. Non-accepted rows may stay unresolved: those are addresses with no source and
no call-site evidence, and the resolver refuses to guess a name for them.

Measured on the current private ledger: 16,073 rows over 18 modules, 11,660
accepted, with 9,485 names from the ledger, 5,102 from source definitions, 193 from
relocation evidence, 85 from definition order, and 151 accepted rows unresolved
(main-module functions whose source defines semantic names that neither carry the
address nor appear in any taken relocation). The text map is stable across runs.
