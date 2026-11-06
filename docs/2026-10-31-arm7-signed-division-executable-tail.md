# Signed ARM7 divide executable tail — 2026-10-31

Original host ARM7 WRAM ARM entry `0x03806C38` spans524 bytes through`0x03806E44`. Independent replay qualifies138 actual signed-numerator/positive-denominator quotient-and-remainder returns and seven byte/mode/range guards. Module SHA-256 is`e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c`; the complete span SHA-256 is`e8183a62ffe6a54210cd7d025b01431ff792025c1b45a0e8537abd8cec16ccfb`.

The computed dispatch reaches all eight targets and all388 ARM instruction bytes in`[0x03806CAC,0x03806E30)`. The four-byte NOP`[0x03806CA8,0x03806CAC)` is skipped. The signed epilogue`[0x03806E30,0x03806E44)` was already inventoried. R0 carries quotient and R1 signed remainder; scratchIP and arithmetic flags are caller-saved. Zero/negative denominators and other exceptional division contracts remain outside this proof.

Reproduce`python arm7_lane_sdk_signed_division_scope_20261031.py`, then`python amend_arm7_signed_division_inventory_20261031.py`. The ROM/processor/program/module/mode/address keyed amendment lives in`ledger/executable-scope-amendments-signed.json`; its separate file preserves the frozen unsigned amendment and that producer's ledger hash/order contract. Consult both scope ledgers alongside the heuristic function inventory. Shared Ghidra/configuration boundaries are unchanged.

This records executable coverage discovery, not decompiled implementation. It adds zero functions, source bytes, assembly-source credit or ROM credit. The initialized-module denominator already includes the tail and stays unchanged. No executable-only global denominator or historical original-assembly provenance is established.
