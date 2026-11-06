# Explicit item-word consumption chance source - 2026-10-30

This is a zero-new-coverage source-quality alternative for already matched main ARM `02065DEC..02065E14`, exactly40 bytes. No primary selection, registry, accepted old source, application file or frozen cohort45 helper was changed.

The preserved old primary is `src/runtime/runtime05/native_main_02065dec.c`, SHA-256 `0ee3a6c6d27deb53059fc51ffc064b3843babf415771e8479a125223d0b61180`. It declares the function `(void)` and calls the item getter without an argument. Its matching ARM instructions retain the incoming item in hardware R0, but its C interface does not express that argument. Instruction equality alone did not establish a portable argument contract.

The explicit alternative is `src/mechanics_save/20261030_item_consume_chance.c`, SHA-256 `72fd5be6d2a188f7f6986b5013ded7565c98e1f1cb8e4563abe61101be0e079c`. It accepts a signed32-bit item word, calls typed `getter(item)`, and returns whether descriptor byte+0x25 is greater than the signed bounded-RNG result for bound100. Pinned2base O2 speed yields the complete original40-byte span after real MW linking. Object SHA-256 is `b3dc5e6f6547fcfa4da2ca32f7009eea970a18b076d6302e58ddcdf9bfe0c259`; native/linked span SHA-256 is `c2682c1fbd3e13f4fdfc5b263d062d3b292c7f0b60c4675c92abef54e1e2c10b`.

Canonical replay:

```powershell
& C:/Users/trevo/AppData/Local/Programs/Python/Python313/python.exe C:/Users/trevo/Documents/RecProgramming/DQM/dqmj2pro-decomp/match_mechanics_save_20261030_item_consume_chance.py
```

The verifier accepts an explicit repository-relative `--source` path while pinning contents. Its canonical report is `evidence/matches/mechanics-save-20261030-item-consume-chance.json`, SHA-256 `5c67da71f2e31c108b201ad3bff13f34e6c2cce78c45f60d1f1155723a625ff8`. Complete current native bytes, source/object identities, pinned successful real-link evidence and exact acceptance fields are checked. The report proposes an audited primary migration and explicitly records zero new functions/bytes and40 reused bytes.

`evidence/application/item-consume-chance-fixtures-20261030.json`, SHA-256 `77902b9d302cb997138c80437dab15a2c904a1f9c96f3345e7afd526a50c96d1`, contains2,520 cases and5,040 original/compiled helper returns, plus104 standalone original bounded-RNG controls:5,144 actual host returns. The5,040 nested RNG returns are recorded separately and not added again. There are no callee providers; the original getter and RNG execute.

The independent model computes the wrapped32-bit step `state = state*1103515245 + 12345`, then `(state >> 16) % 100`. Modular-inverse seed construction covers every result0..99. Synthetic threshold bytes0/1/99/100/255 are tested at item IDs0/48/254. All255 physical descriptor IDs additionally use seeds0/1/12345/FFFFFFFF. The model checks strict comparison, exact next state, the actual forwarded item word/getter pointer, bound100 and the returned random result. Only one RNG-word write occurs; all saved bytes and the entire descriptor table remain unchanged.

Threshold0 is never true;100 and255 are always true over the supported bounded results. Every call still advances RNG exactly once, including those endpoint thresholds. This helper decides a chance and does not itself debit inventory. The native book replacement proof independently establishes how book48's threshold100 result feeds the later single debit.

Invalid item IDs and general bounded-RNG values other than100 remain outside this interface proof. Adopting the alternative requires the integrator to check the old primary identity, preserve old evidence, select the explicit source and rerun full module/source/ROM/regression gates with no coverage increase. No migration is performed by this verifier.
