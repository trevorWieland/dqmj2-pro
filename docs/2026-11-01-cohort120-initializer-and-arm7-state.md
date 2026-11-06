# Initializer, ARM7 state, and a measured reinterpret frontend — 2026-11-01

This individual planning scope is consolidated into [the active expanded119 transaction](2026-11-01-cohort119-expanded-source-and-native-components.md). Its original source/native measurements remain separate.

ROM identity is SHA-256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`. This package proposes three ordinary C functions covering376 initialized bytes, with no denominator increase. Acceptance requires the prior committed closure and all new/current module checks. The separate native helper, boundary and compiler probes add no source bytes.

## Main ARM 02037DC8 / 136

The compatible source returns the word address `020F1F64`, takes no explicit inputs, and initializes the record only when its word at+12 is zero. The original generated source already matched134 bytes; changing the compatible byte assignment at+0 from unsigned to signed storage reproduces the native `MVN` rather than a truncated positive immediate. This proves the low-byte store and emitted bytes, not historical field signedness.

The initializer sets word+12 to1, installs callback addresses `02037FAC` at+16 and `02037FE4` at+28, clears words+20/+32, forwards those two field addresses to registration wrappers, initializes additional global records, and finally stores byte255 at+0 and word1 at+4. All other record bytes remain unchanged in the supported test context.

`python match_main_signed_store136_20261101.py` freshly compiles and genuinely links116 code bytes plus20 generated pool bytes. It executes512 paired contexts,1,024 actual entry returns,1,536 separately counted original helper returns, and1,536 explicitly supplied calls. Native helpers `020094B4`, `020389D8` and `02037750` execute; the first is restricted to its already-initialized lower flag branch. The two registration wrappers and larger initializer remain supplied boundaries with no external effects. The caller receives no helper source credit.

The independent model checks the full nonstack main-memory image, pointer/callback/state fields, relevant registers, flags, stack guards and ordered effects. Each of two whole wrong C variants returns128 times:64 affected initialization paths are rejected and64 early-return paths remain unchanged. A bounded prefix cannot count as return. Replaying from a different working directory with `-I -S` reproduces the canonical report byte-for-byte. Callback invocation, first-time lower initialization, queues, threads, concurrency and full startup remain unproved.

## Host ARM7/main ARM 027E9C58 / 104 and 027E9D00 / 136

The frozen state240 packet reconstructs200 instruction bytes and40 generated literal bytes. It includes976 actual original/compiled owned returns and976 separate original fill returns. Its1,528 scoped helper events include84 overlapping tail observations and must not be counted as distinct independent top returns. The constructor producer remains a prefix with zero completed-constructor credit.

The caller-specific linker permits the descriptor-produced word at `0380FFF4` only for these two processor/program/module/mode/address/source-hash identities. It freshly reproduces the existing descriptor-producer witness. No blanket pointer-cast exception is introduced: original/default policies, previous source guards and unrelated callers retain their refusals. `python validate_arm7_core117_state240_20261101.py` executes58 metadata controls,42 direct source/ownership/producer/default-policy controls and eight native controls. Wrong compiled C returns640 times and fails its independent model308 times, with332 explicit unchanged positives.

`python validate_arm7_core117_gap52_20261101.py` separately qualifies the discovered original52-byte helper with144 native runs and32 controls. Its inventory/configuration/denominator/source credit remains zero pending boundary adoption and reconstruction. Producer storage, referenced data and native helper bytes do not become source credit through this packet. See the worker's frozen dated state240 and gap52 writeups for exact ABI, MMIO and path limits.

## f32/s32 bit reinterpretation frontend

The pinned m2c translator emits `M2C_BITWISE` when its reinterpret cast crosses float/integer types. Its bundled valid-syntax macro uses an ordinary numeric cast as a placeholder. That placeholder does not establish the desired bit interpretation and is not adopted.

`lower_same_width_float_bitcasts_20261101.py` accepts only explicit same-width f32/s32 operands. Function return types must be supplied from qualified context; unknown or differing-width operands fail. Proven inverse pairs cancel. Other cases use a width-checked union compound literal. Strings remain unchanged, and other unresolved arithmetic, carry, stack and type placeholders remain unsupported. No existing translator or matched source is edited.

`python probe_same_width_bitcasts_20261101.py` tests32 configurations: four primitive casts/pairs across four pinned compilers and ARM9/ARM7 soft-float targets. It requires4,608 actual raw-bit returns, including signed zeros, infinities, NaN payloads, subnormals and deterministic random words. A wrong-bit source actually returns144 times and is rejected144 times; four syntax/width qualification controls also reject. The primitive probes contain no relocations or providers and must return within their bound.

These are synthetic compiler/ABI probes with zero game-byte credit. Union compound literals can add private stack traffic; the simple probe is20 bytes under one compiler. Full caller compilation, genuine linking and independent native effects still decide whether a reconstructed game routine is correct or matching. No Windows or Android floating-call ABI is established here. The module was supplied to the overlay worker as a conditional frontend improvement.

## Clean-checkout dependency evidence

The source106 materialized checkout retained its original908 failure and the subsequent922 failure. After the card452 prerequisite was rebuilt, original commands908..921 passed. Step922 then found missing object files for an unselected historical alarm-registration oracle. `reproduce_alarm_registration156_current_products_20261101.py` executes the original matcher and all50 original controls through the separately sealed closure mechanism. It edits no frozen matcher/validator source. The v2 continuation retains all original reports/log hashes and resumes remaining original commands from922.

These explicit prerequisites repair the replay dependency order. A continuation must finish all original remaining commands and compare the exact ROM before receiving even a continued-checkout pass. It is not an uninterrupted clean replay, a source-only ROM, a full Windows game or Android/Thor execution.
