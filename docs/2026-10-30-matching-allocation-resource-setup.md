# Matching allocation resource setup

Main ARM`020787A0..02078804` is a new100-byte ordinary-C candidate, pending integrator acceptance. The complete native body matches both compiled/linker output and128 actual native/C returns across64 cases. Canonical `evidence/matches/mechanics-save-20261030-allocation-resource-setup.json` SHA-256`d4bea9dcb28d633be9007a60114302dc8fc2ea5ce3b60fdf2ff9b00b3386816f` is stable from normal and unrelated working directories.

```text
python match_mechanics_save_20261030_allocation_resource_setup.py
```

The matcher accepts an explicit repository-relative `--source`, default `src/mechanics_save/20261030_allocation_resource_setup/allocation_resource_setup.c`, source SHA-256`925c3d3183825d8c403885894329cca7e590818f04afd233e5336ecfd95df31c`; its included header SHA-256 is`bfa80125d199c5dbe7dcea7c600e39d391fc992a4efb264a8db69b208a2e271d`. O2 space and speed hypotheses both produce all100 exact bytes with the pinned2.0/base compiler and real linker. The chosen source defines an actual four-byte signed-short coordinate pair instead of separate adjacent short locals.

Signature is `u32 setup(void)`. Original overlay getter`02215698` executes and supplies its context word. The measured call sequence is `022159B8(020DE414,4)`, `0204B4F4(context+10,coordinate_pair,200,3,2,36)`, then `0204B61C(context+10,0)`. The coordinate pair contains two zero halfwords; the full final32-bit provider result is forwarded, while earlier provider returns are discarded. Resource-data appearance and success meaning are not inferred from these constants.

The fixture varies resource-load and rectangle-boundary return words independently of the final return0/1/80000000/FFFFFFFF. Half the profiles additionally clobber AAPCS volatile R1/R2/R3/R12 and condition flags after each lower call, while preserving stack/callee-saved contracts. Native/source argument order, complete provider arguments, coordinate bytes, opaque return word and ordered writes match, with saved and allocation state invariant. All runs must actually return within10000 instructions and use fresh machines.

The three lower resource/window functions remain explicit bounded providers; their full physical state effects are not asserted presentation-only. The singleton getter is original native code. No scene reachability, accepted module build, source coverage increment, registry or source-preference mutation occurs in this replay.

This function was canonically unmatched before recovery. Adjacent20-byte`02078804` remains an existing frozen accepted source. The separately investigated164-byte`02078818` uses a full32-bit mode at state021C6234, not the byte dereference guessed by its old m2c context. Its preferred word-mode/common-tail hypothesis remains nonmatching160 bytes, with the coordinate-address lowering unresolved; no padding, volatile, assembly or forced-register workaround is adopted.
