# Cohort 92: codecs, explicit inputs and typed roots

This accepted source increment adds fourteen functions and 1,190 initialized bytes: 9,032 functions and 680,941 bytes, or 27.1006624% of 2,512,636 inventoried initialized module bytes. One 40-byte raw-index interface migration adds zero coverage. The acceptance receipt and complete validation driver record all twenty exact module comparisons, both checksum matches and all 144 isolated returns, 5,117 getter comparisons, retained source matches, and the exact scaffold-assisted ROM hash and length. This is not an overall game completion percentage.

The source packets are two main 32-byte halfword/zero-argument units; save/core Thumb22+68, ARM92+100 and ARM104+76; child ARM7 main124,172,32+44 and120; and overlay001 ARM172. Module, processor, program, mode, full input hashes and boundaries remain explicit in their matching reports.

## Source qualification

[The main halfword/argument writeup](2026-10-31-main-halfword-and-zero-argument.md) records 1,536 native/C returns and 48 returning wrong-C controls. Physical halfword stride, readback and a required zero argument are recovered without register assignments or padding.

The Thumb22 unit scans nonzero halfwords with a two-byte stride. Thumb68 performs five full-word transfers and a mask2 update in measured order. Their 1,120 top returns use no helpers/providers; alias-sensitive backing and canaries are checked. No encoding, status names or lifecycle meaning are inferred.

The two ARM92/100 callers retain full input words, explicit measured byte truncation and coordinate-pointer forwarding. Their packet also replaces the already matched 02049AA8/40 interface: native mode0 performs signed-byte conversion after adding0x24, while the other branch forwards the entire word. The old narrow formal parameter cannot represent both paths portably. The packet's 7,488 top returns include direct lookup/migration cases and caller cases, rather than implying all are new source. Original lookup/pointer helpers execute; four final service/callback boundaries remain supplied.

ARM104 uses separate role-qualified initializer/container views at one measured root address, matching its two distinct native literal words. ARM76 initializes a complete 72-byte object with native store/increment order. Their 800 top returns and alias-sensitive controls preserve complete backing and ordered effects; only CE048 is supplied. The constructor is void. Its physical R0 residue is compared but not promoted to an API return. Original declaration identities remain hypotheses; the aliases do not add padding or data-source credit.

## Child ARM7

The 124-byte caller consumes an explicit unsigned64 ABI word pair from the original divider rather than a generated secondary-register placeholder. Its distinct address-qualified alias preserves an older low-word declaration. There are 896 own returns and 3,584 separately observed divide returns. A separate zero-credit scope report confirms 480 executed bytes inside the divider's484-byte decoded span, including472 outside its configured8-byte entry; skippedNOP4 and division-zero characterization remain explicit. No automatic boundary or denominator extension follows.

The 172-byte record checker preserves its physical two-byte header advance and full-word arithmetic. Its256 own returns include40,576 original byte-getter and40,576 CRC-step returns, separately counted. A narrow immutable-input-verified fork permits only its four-byte incoming descriptor word; no general runtime/BSS guard is relaxed and no table/data credit is requested.

The provider-free32/44 byte getter/writer pair produces5,232 own returns and checks read widths, masks, guarded writes and neighboring bytes. The120-byte CRC primitive produces2,592 own returns, all16 table indexes, full-word high-bit inputs, independent polynomial results and no-write effects. Its original32-byte table is still a dependency with zero source credit in this cohort. Any mathematical table reconstruction is a separate later proposal.

## Overlay and acceptance

Overlay001021F9608/172 uses a natural signed accumulator and staged halfword stores. All156 instruction bytes and16 literal bytes match. Root independently measures3,132 valid caller returns;506 invalid-slot observations have zero top-return credit. Actual native helpers and explicitly supplied lower boundaries remain separately counted. The larger1,352-byte scouting builder remains a functional nonmatching draft and adds no source coverage.

Every prior source selection remains unchanged except the explicit zero-credit 40-byte migration. All required module, checksum, getter, retained-match and exact 175,959,612-byte scaffold-assisted ROM gates passed. A complete source-only ROM, complete Windows game and Android device execution remain unproven. No application/UI/adapters or original inputs are edited.

Reproduce the measured acceptance with `python run_cohort_20261031_92.py` then `python finalize_cohort_20261031_92.py`. A complete fresh-checkout replay of this cohort remains unproven. The registered divider-scope oracle explicitly runs its producer before its validator in a new wrapper, avoiding the historical cache-order defect. Check source registry commands for the individual reproduction and control programs.
