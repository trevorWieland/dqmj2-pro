# Matching allocation bounds facade

Main ARM`020788BC..020788F0` now has an exact52-byte ordinary-C candidate at `src/mechanics_save/20261030_allocation_bounds_facade.c`, source SHA-256`5c8e0a0c42d30a67af66ed6539f7389fa5a70e53a72db6145f9c0b282911f3fb`. Complete native and real MW linked bytes match. Canonical report `evidence/matches/mechanics-save-20261030-allocation-bounds-facade.json` SHA-256 is`05e3b38c6f3df133bc2aa81892ba5ad4ee5e83761f26f064735f36ab42538703`.

```text
python match_mechanics_save_20261030_allocation_bounds_facade.py
```

The matcher accepts a repository-relative `--source`. The source defines the complete8-byte bounds structure and the returned transient subcontext view. Native incoming R0 is forwarded as full rank R1 to `020768D8`, with an actual8-byte stack destination in R0. The facade then copies signed16 lower into`021C6434+E0` and upper into`+E2`, equivalent to allocation state`021C6234+2E0/+2E2`, and returns address`021C6434`. It does not return the bounds helper's equality result.

All3036 frozen bounds profiles are independently regenerated and replayed for original and compiled facade, totaling6072 actual facade host returns. Original276-byte bounds and68-byte last-entry routines execute without providers and each separately returns6072 times. Nested counts are not added to host returns. The typed source fills only those two halfwords in the original order, preserves all other0x500 allocation-state bytes, save/descriptor inputs and preceding descriptor byte, and returns the full expected pointer word.

The profiles retain all physical skill rows, synthetic empty/one/two/ten-entry and unsorted rows, ranks0..10, slots0..4, signed-free extremes, full-word targets, reversed/empty bounds and explicit preceding-byte controls. Output values follow the existing qualified bounds model without target normalization. Other ranks/slots, aliasing destinations, ordinary scene reachability and commit/import policy remain unsupported.

The old draft contained an undeclared `sp2` and only a single-short destination. The recovered C uses a complete bounds object matching the actual callee write extent. Canonical function boundaries and accepted intervals were audited before recovery; no existing source coverage is duplicated. Integrator module/ROM acceptance remains pending, with registry/preferences/accepted build unchanged.
