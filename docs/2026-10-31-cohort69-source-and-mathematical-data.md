# Cohort 69 source and mathematical data — 2026-10-31

The accepted build measures 8,788 functions and 642,225 source-linked initialized module bytes. This adds 11 ordinary C functions totaling 5,260 bytes, plus 16,384 independently generated mathematical data bytes. Four source-primary migrations cover 504 already accepted bytes and receive zero new coverage. All other prior selected source/object identities remain unchanged.

| New source packet | Functions | Initialized bytes |
|---|---:|---:|
| UID/descriptor comparator | 1 | 144 |
| ov001 ability-list caller | 1 | 788 |
| ov006 summary caller | 1 | 508 |
| ARM7 setting writer | 1 | 52 |
| Save-view parts accessor | 1 | 216 |
| ARM7 alarm selector | 1 | 176 |
| ov006 menu controller | 1 | 2,728 |
| ov006 setup caller | 1 | 372 |
| Main trigonometry wrappers | 3 | 276 |
| Q12 sine/cosine table | 0 | 16,384 |

The table comes from 110-digit Decimal arithmetic, Machin's formula, Taylor evaluation, symmetry and nearest-even rounding. Its generator reads no original table bytes. All 8,192 signed Q12 elements match the measured input and compiled/linked data. Data is reported separately from ordinary logic; see [the mathematical reconstruction record](2026-10-31-sdk-trig-mathematical-source.md). The three angle wrappers pass 8,258 provider-free original/source returns, with real Thumb-helper returns counted separately. Whole compiled-C table and wrapper mutations reject as measured.

The four primary migrations replace three signed-shift comparator hypotheses and one raw-word pointer-forwarding hypothesis with qualified C types and native-call contracts. Their historical source versions remain unchanged. All 24 preferred source inputs are actually selected and linked. The standalone utility child-counter proof contributes no new source bytes because its function was already accepted; an initially duplicated registration failed the utility overlap gate and was removed before acceptance. Both refusal and correction remain in evidence/attempts.

All 20 initialized module comparisons and the exact 175,959,612-byte ROM comparison pass, with SHA-256 674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6. The existing two checksum matches, 36 vectors and 144 isolated actual returns pass. Getter replay still passes 5,117 comparisons. Evidence freshness rejection tests and authored-source policy pass. The 16-command integration run is recorded in evidence/verification/cohort69-validation-driver.json; measured acceptance is in cohort-2026-10-29-69.json. Reproduce using python run_cohort_20261031_69.py and python finalize_cohort_20261031_69.py.

Native proofs retain their limits: the setting-pointer global is a measured four-byte descriptor-produced cell, not inferred BSS coverage; the view accessor excludes active-state paths; menu and summary proofs still declare their synthetic UI providers. The setup caller covers CPU-copy fallback using a synthetic DMA setting and zero-length file returns, with default DMA wait and positive file lengths unsupported. The ability native-consumer proof covers its declared no-modifier skill subset. None establishes bank chronology or complete save serialization.

The 25.5598% figure divides 642,225 by the 2,512,636-byte initialized module footprint. It includes 621,490 function bytes with associated pools, 20,711 source data bytes and 24 padding bytes. Unresolved initialized coverage is 1,870,411 bytes. This is neither overall game completion nor a proven executable-only percentage. Original executable gaps remain scaffolding; source-only ROM completion, a complete Windows game, Android device execution and a fresh full-suite replay of this exact cohort remain unproven.

Original inputs and baseline hashes remain unchanged. The separate application snapshot contains outside changes, so strict whole-workspace isolation remains false. Those changes were not restored or rebaselined. Independent clean checkouts S and T are still running older immutable cohorts and do not certify cohort69.

The next unregistered source queue has a 1,400-byte UTF16 format parser with 5,572 provider-free original/source returns and 24 returning negative-control executions, plus a 100-byte bank-zero header-summary wrapper with 1,168 original/source returns. Full module gates remain necessary before either earns accepted coverage. The save wrapper reads index zero and does not establish active-bank selection.
