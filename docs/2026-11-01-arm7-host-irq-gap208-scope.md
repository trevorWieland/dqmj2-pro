# ARM7 host IRQ callable entries and reserved words - 2026-11-01

This read-only witness identifies eight 16-byte ARM wrappers at `037FB6C8` through `037FB738`, plus an 80-byte callable handler at `037FB748`. Their 208 bytes are already initialized. Source, data, assembly and denominator credit remain zero; shared configuration, default guards and accepted sources are unchanged.

## Boundary reconciliation

The initialized 25-word IRQ table at `03807564` names every entry. Each wrapper contains 12 instruction bytes and a 4-byte dispatcher literal. The handler contains 68 instruction bytes and 12 literal bytes. None has alignment padding. The configured dispatcher at `037FB63C` adds 120 instruction and 20 literal bytes to this 348-byte connected group.

Ghidra already associates `037FB748..037FB78C` with ISR `037FB488`, whose discontiguous ranges are `037FB488..037FB4EC` and `037FB748..037FB78C`. Thus only the eight wrappers' 128 bytes are wholly outside configured ranges. The handler has that existing 68-byte code association plus 12 literal bytes. The rejected initial blanket classification is preserved in the draft reconciliation receipt. The separate vector root establishes callability without removing the association or granting unique byte ownership. No boundary amendment is installed; future coverage must avoid counting shared bytes twice.

The static scan covers aligned words in all three initialized host ARM7 modules and direct branches in known instruction ranges. It reconciles the handler's own interior branch. Computed references, runtime vector changes and other processors remain outside exhaustive coverage.

## Native evidence

There are 204 actual body returns: 12 for each wrapper, 12 for the handler and 96 for the existing dispatcher. The 108 new-entry observations have zero source credit. Real initializer `037FB798` and callback producer `037FB7BC` contribute 408 separately counted returns. After those prefixes, fixtures deliberately alter enabled flags, counters, timers, IME, IE and check-word state.

All 284 instruction bytes of the connected group were visited. Full mapped non-stack memory and ordered writes match an independent model. Separate callback returns total 102: 96 timer callbacks and six original dummy calls. The 96 timer-writer tail transfers are not additional callback returns. Timer reset zero/nonzero paths each have 48 callback returns. There are no provider substitutions. An exhausted wrapper has zero return or post-state credit.

Execution is synchronous with register-shadow MMIO. It does not prove hardware exception delivery, W1C behavior, concurrency, scene reachability, arbitrary callbacks or malformed-index safety. Wrappers provide indexes 0-7; the handler uses record 8.

## Fixed-word qualification limits

`0380FFF8` has 204 measured four-byte reads and 204 OR writes. `027FFC3C` has 12 measured four-byte read/increment/write observations including unsigned wrap, plus 204 separate initializer zero writes. Both are outside measured initialized/BSS ownership. No module-data or extent credit follows. Default ordinary-data guards still refuse both addresses.

Git-blob-verified `pret/pokediamond` commit `b623abef1b4dfe204ca50aab42447ac00c134290` supports the table, callback flow and reserved roles. Its ARM7 map computes the check word as `03810000 - 40 + 38 = 0380FFF8` and expresses the counter as `HW_MAIN_MEM + 007FFC3C`. The complete include closure defining `HW_MAIN_MEM` is not supplied; the game's literal and executed address are measured independently. This reference is source-specific, not assigned CC0. Same historical SDK revision and original assembly authorship remain unproved.

The word receipt names exact callers and four-byte addresses. It grants no source binding, neighboring address, general absolute-pointer exception or physical mirror/coherence guarantee.

## Reproduction

Run `python reproduce_arm7_host_irq_gap208_witness_20261101.py` from any working directory. It verifies six frozen producer/validator hashes, regenerates native products before validators, and checks four canonical report hashes. There are no compiled-object or unaccepted-source cache inputs. Native traces use deterministic mtime-zero gzip with raw and compressed hashes.

The scope suite has 42 negative controls and the word suite has 29. They reject altered identities, modes, extents, shared associations, literal roles, products, actual returns, tail counts, source credit and address permissions. The read-only engine rejects executable replacement bodies. Both suites restore positive validation.

Ten separate ordinary C drafts compile; the configured dispatcher genuinely links, while nine new entries retain canonical-entry refusals. Those drafts are excluded from this read-only transport and accepted source. Source proofs and any narrow admission adapter need separate review.
