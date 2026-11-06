# Read-only void-tail pointer audit - 2026-10-31

This is a narrow static proof frontier,not a source migration or defect count. Replay `python audit_save_core_void_tail_pointers_20261031.py`. The recorded local report SHA isebce0f78e8c3bb609d4978ac9224fd8988ce8808c9aae4988d8c90c9d3d30400. It uses immutable normalized89 identities and requires each locally present selected source hash to match;missing/newly unavailable source paths are outside this local scan. No source/config/ledger is changed.

The92 locally present simple void-return definitions must have an actual unconditional tail preserving incomingR0. Only a literal scratch-register BX or direct branch is admitted. Its target must reach an unconditional fixed-offset data load through incomingR0 or a tracked alias,before any conditional,unknown or nontrivial prefix. A raw register read alone never qualifies. Native mode,addresses,hashes,source identity and exact load PC are recorded. This is deliberately conservative and does not analyze complex/conditional wrappers.

| Wrapper | Tail target | Qualified read PC | Source ownership |
|---|---|---|---|
| 0x20384f8 | 0x20387a8 | 0x20387b0 | Root range,read only |
| 0x203c940 | 0x20293c8 | 0x20293d4 | Root range,read only |
| 0x203c94c | 0x20294cc | 0x20294d8 | Root range,read only |
| 0x204b61c | 0x204b380 | 0x204b388 | Owned range |
| 0x204b770 | 0x204b380 | 0x204b388 | Owned range |
| 0x205fd28 | 0x20068c0 | 0x20068c0 | Owned range |
| 0x2094274 | 0x200cb10 | 0x200cb18 | Owned range |
| 0x20971ac | 0x2097198 | 0x2096ce8 | Owned range |
| 0x20972a0 | 0x20972a8 | 0x20972a8 | Owned range |

There are9 static leads and zero proven native/C defects or new coverage. Three wrappers below02040000 remain outside this worker source ownership. The six already qualified140-byte pointer alternatives are excluded. Every lead still needs a bounded native dereference witness on distinct disposable pointers,caller-dependent controls,typed-source/compiler/real-link equality and explicit ordinary-context limits. The report does not authorize changing any primary.

Positive96D9C reaches the existingCE8 unconditional load. Explicit485B4 and literal-input41800 controls are rejected:the former has an unqualified conditional path,the latter replaces incomingR0. Thus the prior correlated-condition counterexample is not reclassified from raw reads. Sixty-five other prefixes remain nontrivial/unproved and18 are conditional before the proposed pointer read.

The audit covers only the selected89 mainARM9 source paths available with matching hashes in this lane. Re-running against a different accessible file set can extend the frontier;this report is not a whole-project completeness claim. No old source,original ROM/save/application,bank meaning or source credit changes.
