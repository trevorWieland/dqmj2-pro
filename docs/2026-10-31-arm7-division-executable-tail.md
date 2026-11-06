# ARM7 division executable-tail amendment — 2026-10-31

The connected SDK-flow proof reaches original host ARM7 WRAM helper `0x03806E4C`. A prior strict function inventory stops before a computed unrolled tail. Integrator replay confirms the module SHA e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c and the complete 476-byte helper-region SHA `5c91d1640b64a99527e9faff2db6a08378db2a9324a7c1a3ca5dc765b7671f07`.

The instruction at `0x03806E98` computes one of eight actual entry targets, `0x03806EA0 + 48*k` for k = 0..7. The four-byte NOP at `0x03806E9C` is skipped. The executed tail `0x03806EA0..0x03807028` contains 392 instruction bytes: 32 verified carry/subtract triples and the final move/return. All eight dispatch targets and the complete additional instruction range are observed across 152 actual quotient/remainder returns. Seven guards reject altered range/mode/byte assumptions. No BIOS or helper-result provider is used.

Ledger/executable-scope-amendments.json records build hash, processor, program, module, ARM mode, input/source evidence hashes, executed range and excluded NOP separately. The original candidate-boundary files are unchanged. The qualified476-byte span is not adopted as reconstructed source or a general function-boundary rule. There is zero new function, C, assembly, blob or matched-byte credit.

This range already lies inside the measured initialized ARM7 module. The 2,512,636-byte initialized denominator therefore stays unchanged. A complete executable-only denominator still is not proven. Positive-denominator u32 quotient/remainder cases do not establish all possible helper inputs or historical original assembly provenance.

Reproduce with python arm7_lane_sdk_division_scope_20261031.py followed by python amend_arm7_division_inventory_20261031.py. The original strict-inventory refusal is retained in the flow328 packet. The amendment allows verified execution coverage to be reported honestly without rewriting frozen analyses or increasing source progress.
