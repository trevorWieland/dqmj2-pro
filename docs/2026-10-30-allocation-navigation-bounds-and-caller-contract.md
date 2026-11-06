# Allocation navigation bounds and caller contract

Two new ordinary-C functions reproduce344 native ARM9 main bytes after pinned compilation and genuine MW linking. The canonical report is `evidence/matches/mechanics-save-20261030-allocation-bounds.json`, SHA-256 `ae5297ea357c61547e7cbb0d131506ce865ba124fe9b8884c59b4aa15d6864fb`, identical for normal and unrelated-working-directory replays. They require integrator module/ROM acceptance; these scripts do not register source or update coverage.

| Function | Preferred source | Source SHA-256 | Object SHA-256 |
| --- | --- | --- | --- |
|main ARM`020768D8..020769EC`,276B|`src/mechanics_save/20261030_allocation_bounds.c`|`5105392d65813c3b47077c6d8620489371eb930bb5bdf0b012511c2d9ebc7825`|`4a49e9874d595a12cbd51b6252c75bfe5f4d031a401c5bb85e1a997f4cc37d05`|
|main ARM`0207AD3C..0207AD80`,68B|`src/mechanics_save/20261030_skill_last_entry.c`|`e9950ac494900ecb0db14886af504ba6ebcd23078a409df014cd45678ba7d036`|`fda95612da98b69c91262ee2c98023b0f5665e0ac76fc3b7c1ddf184b2034fb0`|

Native and linked body hashes are respectively `26606d7ad04bef4542151ca6b839f37abd64f7d9e5a4616aa368283c8a8667af` and `01b97a55c3bed6a892c03fede491a44bb59280a467df2c352276637e90ae73b1`. Compiler2.0/base SHA-256 `7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880` uses the complete O2/speed flags recorded in the report, with the existing local license. The actual linker SHA-256 is `bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74`. Original ROM/save hashes are revalidated before and after fixtures. Canonical interval audits found no accepted source overlap for either function before their recovery.

## Eight-byte range construction

The276-byte function takes `(AllocationBounds *output, int rank)`. The exact output layout is signed16 upper/lower/next at offsets0/2/4, followed by lower-equality and upper-equality bytes at6/7. It reads context`021C6234`: selected slot at+`0xFC`, record pointer at+`0x1EC`, target word at+`0x250`, and descriptor-pointer array`021C64D0`. Record free points at+`0x3C` are signed16; allocated points are the unsigned byte at record+`0x7B`+2*slot.

The operation order is measured:

1. Select lower and following descriptor thresholds using rank and the original last-entry getter.
2. Copy the following threshold to initial upper. The separate next field retains that uncapped threshold.
3. When the current target equals the initial lower, move lower back to the earlier threshold, or0 for rank≤1.
4. Floor lower to the allocated byte.
5. Cap upper to allocated + signed16 free points.
6. Store equality with the current full-word target, upper first and lower second.

The routine preserves empty and reversed ranges. It does not normalize upper below lower, mutate the target or deduct points. Its measured full-word R0 on return is lower equality. The original`020769EC` caller ignores that word; no historical return declaration or broader API meaning follows.

`allocation-bounds-fixtures-20261030.json`, SHA-256 `6d63044b31c93833a205718ef892ccfe6c0b31ba9ce22de3ca551d5f3df13c95`, contains3036 cases and6072 actual native/source returns. They include signed free0/1/32767/−32768/−1, ranks0..10, slots0..4, allocated0/10/255, full-word targets, aligned output with surrounding guards, every physical skill row and explicit synthetic malformed rows.2547 cases produce reversed ranges and360 empty ranges. The complete output, ordered writes and original getter contract are compared; saved/context/descriptor inputs stay invariant.

An empty/one-entry descriptor combined with forged rank1 can read one byte immediately before the descriptor. The bounded fixtures explicitly vary that byte through0/127/255 and report it; it is not silently replaced by the descriptor's last byte. These malformed context tests require the preceding byte to be mapped. They establish neither safe arbitrary descriptors nor an import prohibition.

## Last-entry getter

The68-byte function reads at most10 entries. A zero threshold stops before action/feature access. Otherwise the first action byte, or its fallback feature byte, must be nonzero. The full-word result is `max(0,count-1)`, so empty and single-entry prefixes both return0.

`skill-last-entry-fixtures-20261030.json`, SHA-256 `386b42ed749b34ddd42b2eaa366fc1d3fc604a068927e9f95ccac14c75dc5359`, contains553 cases and1106 actual native/source returns. It covers all256 physical skill rows plus synthetic early holes with populated tails, feature-only rows, action words whose upper bytes alone are nonzero, and byte values1/128/255. Exact ordered byte-read addresses/widths/values are modeled, and no writes occur. Null/unmapped pointers remain unsupported.

An initial independent model omitted zero-threshold stopping and expected unsigned−1 for an empty descriptor. Native execution rejected it before acceptance. Its generator and rejection record are preserved as `evidence/attempts/allocation-bounds-empty-last-model-20261030.py` and `.json`. Earlier frozen positive-threshold fixtures remain unchanged.

## Original allocation caller and R9

The upstream1516-byte caller`0207726C..02077858` and864-byte cursor controller`020769EC..02076D4C` remain nonmatching. The first has a typed1560-byte hypothesis reusing historical source, with corrected word-wide pointer arrays, record/byte pointer fields and explicit record-ID forwarding. It receives zero exact source credit. Its44-byte overflow includes12 executable tail bytes and32 data bytes, and is not substituted in the native proof below.

`evidence/application/allocation_caller_r9_20261030.py` executes the original1516-byte caller in state5, its original cursor controller, bounds constructor and accepted state setter. Forty-eight top-level caller returns are separate from48 nested cursor returns. Report `allocation-caller-r9-20261030.json` has SHA-256 `fc7c6db14c8559edb1b04ded50b406d724a3ec051ee092f9fff9a86bd8006b07`, stable under unrelated-working-directory replay.

Every nested cursor entry has R9=0 under this original caller. This matters because the cursor's direct A/B paths retain incoming R9 before a later test; arbitrary standalone register states remain unresolved. No fake C argument or assembly shim was introduced to conceal that dependence.

The synthetic profiles use skill22, allocated17, slot0/4, signed free0/−1, target17/22, A/B/both keys and overlay flag bytes7/FF. A wins over B, transitions to6 and keeps the target; its nested return0 suppresses caller view refresh. B transitions to3 and keeps the target; nested return1 causes one caller view refresh. The caller itself returns the sign-extended overlay byte, not an allocation success indicator. Saved state stays invariant because the subsequent commit frame is not executed.

The native cursor invokes navigation value adjustment only on non-A/B paths. The range builder therefore does not impose an unconditional commit/import limit: a directly injected A frame preserves even a forged target. Ordinary constructor/menu reachability and navigation behavior require separate proof. Object/display/widget and slot-view refresh providers are explicit and may have unmodeled constructor/state effects; their substitution cannot establish eligibility prerequisites.

Reproduce:

```text
python match_mechanics_save_20261030_allocation_bounds.py
python evidence/application/allocation_caller_r9_20261030.py
```

The matcher accepts explicit repository-relative `--bounds-source` and `--count-source` paths with the pinned bytes, requires source/object/link identity and complete original-byte equality, and emits qualified native symbol dependencies. Combined exact-function fixtures have3589 cases and7178 actual host returns; nested getter returns are excluded from that total. Original inputs, baseline and application remain untouched, and module/whole-ROM acceptance stays with the integrator.
