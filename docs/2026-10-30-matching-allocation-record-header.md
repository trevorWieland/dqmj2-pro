# Matching allocation record header

Main ARM`020780B0..02078208` is a new344-byte ordinary-C candidate with complete native/object-real-link byte equality and512 paired bounded cases,1024 actual returns. It was confirmed unmatched in `collect_matches` and bounded by the canonical configured function before isolated recovery. It is pending integrator acceptance; no shared registry, source preference or accepted build was edited.

Canonical report `evidence/matches/mechanics-save-20261030-allocation-header.json` SHA-256 is`bf936dd3631918af85da5b7716cb679757087ce52cd7b4619ab6d61d140d12cb`, stable from the repository and an unrelated working directory. Reproduce with pinned Python3.13.5:

```text
python match_mechanics_save_20261030_allocation_header.py
```

The matcher accepts `--source` with an explicit repository-relative path, defaulting to `src/mechanics_save/20261030_allocation_header/allocation_header.c`. Its source is byte-identical to the exact isolated hypothesis, SHA-256`8c9a8e7521188c883b61bb108a8e75aa0fcacb42a36ee78895dc5bbeeddb160e`; header SHA-256`749a9b01d61ee2fe91f82d566e6c044030d893d4af2c769759fd5778d5b726a4`; object SHA-256`2e1c43e60e03178e9c25d1bc2887f9a2d31b85c307680093a0df68c3fd366437`. Native and actual linked body SHA-256 are both`79cdfc00e54566560b16c5628f5d66a48f6676e77500598af31f615f291af605`.

The verified compiler is2.0/base, SHA-256`7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880`; this unit requires the recorded O2 speed preference. O2 space compiled340 bytes and merged the conditional epilogue; O2/O3/O4 speed compiled344 with only coordinate-initialization scheduling differences. Initializing the guaranteed four-byte signed-short coordinate pair's Y before X produces the exact native scheduling, while actual stores remain X then Y. No artificial register forcing or instruction patching is used. Failed variants and profile results remain in `work/mechanics-save/20261030-allocation-renderer/header-*-hypotheses.json` and their unique nonmatching sources.

Signature is `u32 header(s32 display_value)`. It reads the record pointer at allocation state`021C6234+1EC`, obtains UI node1 as a full pointer-to-pointer, and forwards record species+18, the record pointer and the display word to explicit lower formatting/render boundaries. The native footer passes its record signed16 free-point value from+3C, sign-extended to32 bits. The recovered header forwards the entire argument word and does not clamp it.

The header reads the full32-bit identifier at record+14. Original facade`02063FA0` tail-calls`02062650`, which rejects ID0 then searches three words at`021BD524+1C`; facade`02063FAC` similarly calls`02062690`, searching three words at base+28. These are the active and reserve ID-list ranges`021BD540..021BD54B` and`021BD54C..021BD557`. Under the already measured main-block mapping `save[90:3A68] ->021BD51C`, these correspond to bank-relative bytesB4..BF andC0..CB. This mapping does not select a physical bank.

An active-list hit chooses native overlay0 resource descriptor`0221742C(7)`; otherwise a reserve-list hit chooses descriptor8. When both contain the identifier, the active hit wins. A nonzero descriptor is passed to bounded rendering boundary`02065818(descriptor,3,3)`, and its full32-bit return is forwarded. With neither hit, the return is the original second search's0. Membership-icon appearance is an interpretation of this resource use; pixels are not rendered here. The measured descriptor selection does not establish ownership, preparation eligibility or an import policy.

The fixture keeps both native search routines, their facade branches, the native overlay descriptor getter and native UI-node accessor. It varies ID0/1/2/17/255/7FFFFFFF/80000000/FFFFFFFF, absent/active/reserve/both profiles covering all three list slots, signed-free inputs0/1/8000/FFFF, and opaque draw return words0/1/80000000/FFFFFFFF. Every native/C pair uses fresh machine state, actually returns, forwards the expected full display/return words, preserves serialized and allocation state, and matches all provider arguments and ordered writes. Original ROM/save files are revalidated before/after the canonical replay.

Formatting/resource/draw providers remain explicit lower boundaries from the frozen constructor fixture. Deterministic roster/record states do not establish ordinary scene reachability or valid-save requirements. The standalone exact candidate still requires accepted all-source module/ROM regression gates.
