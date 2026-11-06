# C recovery through measured ARM/Thumb linking

The three frozen reports `main-linked-interworking-20261029-main.json`, `main-linked-near-20261029-main.json` and `ov006-linked-near-20261029-ov006.json` under `evidence/matches/` contain 145 ordinary C functions and 9,494 initialized caller bytes. These are isolated compiler-and-linker matches. Whole-module integration and the accepted-build ledger remain separate gates.

The earlier comparator resolved relocation displacements while preserving a pre-link BL encoding. It also treated some function-address literals as even addresses without a Thumb function mapping. Consequently correct C hypotheses could differ from native BLX encodings or tagged function pointers. Recovery does not patch those instruction bytes, mask linked differences or reinterpret successful repacking as source recovery.

`recover_linked_runtime.py` first tests the historical compiled hypothesis with the pinned real `mwldarm`, freezes ordinary C into a unique source directory, recompiles it with the recorded compiler/profile, then independently links and compares every caller byte. Function dependencies name the processor, module, canonical even address and configured instruction mode. Function bindings use zero-sized symbols in uninitialized mode anchors; they contribute no initialized callee instructions or source credit. Original REL/RELA types, addends and encoded instruction fields reach the actual linker unchanged. Content-addressed link snapshots retain the source object, split object, control file, linked ELF, caller image, binding objects and validation hashes.

The initial 90-candidate interworking set produced 84 exact functions. Six linked callers still differ and remain rejected. A broader same-size near-match set produced six additional main functions and 55 overlay006 functions. Failed hypotheses and their genuine linker outputs remain under the report attempt lists and private work directories. Candidate selection itself receives zero credit.

Reproduction uses the frozen C and repository-local inputs/tools, independently of the original draft work directories:

```powershell
python recover_linked_runtime.py --module main --batch linked-interworking-20261029-main --verify
python recover_linked_runtime.py --module main --batch linked-near-20261029-main --verify
python recover_linked_runtime.py --module ov006 --batch linked-near-20261029-ov006 --verify
```

The isolated fixtures report 3,574 returning cases and 7,148 fresh native/C executions, including full observed registers, flags, ordered stores, external-call arguments and fixture-memory hashes. Entered function dependencies must have their configured ARM/Thumb mode; synthetic providers restore the return mode indicated by LR. All supported fixtures require actual return within the bound. There are 1,066 unsupported native fixtures, and 17 functions have no supported generic fixture. Those limitations remain explicit; timeout, invalid native memory and missing game context never count as successful execution. Synthetic providers do not establish physical callee behavior, valid game object domains or semantic field names.

`evidence/verification/interworking-identity-negatives-20261029.json` records rejection of wrong CPU, module, instruction mode and ROM identities. The module builder propagates each source unit's typed bindings to real configured or reconstructed target symbols, preserving overlay namespaces and linker instruction-mode information. Its full-module comparisons, source-scope freshness checks, old matches, ROM construction and clean-checkout reproduction must still pass before coverage is reported as linked.
