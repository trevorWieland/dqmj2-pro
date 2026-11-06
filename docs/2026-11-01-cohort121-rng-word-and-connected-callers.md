# RNG word and connected callers — 2026-11-01

This individual planning scope is consolidated into [the active expanded119 transaction](2026-11-01-cohort119-expanded-source-and-native-components.md). Its original source/native measurements remain separate.

The measured input is ROM SHA-256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`. Three new ordinary C functions propose716 initialized bytes. All new ranges are checked against accepted116 and pending117..120. No data, constructor-prefix, assembly or denominator credit is added. Pending matches remain distinct from accepted module/ROM evidence.

## Main ARM 0203D158 / 152

The compatible signature is unsigned word function(unsigned word selector). It calls the actual main RNG at `0203D294 / 72`, which updates word `020F6044` by `state = state*0x41C64E6D +12345` modulo2^32 and returns `(state>>16)%positive_limit`. The RNG source was already reconstructed; this package adds no RNG-helper bytes. The current word predicate at `0203D1F0 / 68` was also already reconstructed.

For nonzero selector, two draws with limit256 produce bytes a/b. The function stores and returns `a | (b<<8) | (((a*~b+123)&65535)<<16)` at `020F6034`. For selector zero, it draws twice with limit65535, multiplies the incremented draws modulo2^32, stores that product, and repeats while its upper halfword equals `(low_byte * ~second_byte +123)&65535`. These are measured operations and an encoded-word relation. They do not name a scene, persistence role, availability predicate or player-controlled RNG outcome.

The earlier generated C matched144/152 bytes and used a potentially overflowing signed left shift. Eighteen bounded ordinary expression/local-lifetime trials retain all failures. A separate unsigned high-half shift and explicit halfword local produce full152-byte genuine links in12 variants. The selected variant uses no forced registers, assembly or patched bytes; the144 code bytes and eight generated pool bytes match completely.

`python match_main_random_word152_20261101.py` executes512 paired contexts,1,024 actual owned returns and4,444 separate real native helper returns, with zero providers. Original RNG, encoded-word predicate and unsigned division at `02026350 / 484` execute. An independent scalar model compares every draw, seed transition, retry decision, returned word and ordered nonstack write, plus native/source registers, flags, full synthetic state page and stack guards. Eight deterministically found seeds force an actual retry. A complete wrong encoding source returns128 times, with90 model rejects and38 unchanged positives. A bounded prefix fails completion. An unrelated-CWD `-I -S` replay reproduces identical canonical report bytes.

Synthetic state is not an observed future session seed. Arbitrary nontermination, concurrent RNG mutation, complete scenes and the historical meaning of the encoded word remain unproved. The original save and application files are not edited.

## Host ARM7/main ARM 027E91BC / 176

The new C function emits168 code bytes and eight generated pool bytes with full genuine link equality. Its two unsigned word arguments agree with the previously frozen104-byte caller declaration. Raw full-word predicates and unsigned halfword stores remain explicit. The exact-source/identity-gated linker permits the descriptor-produced `0380FFF4` only for this new caller, preserving the original/default and earlier240 policy refusals.

`python validate_arm7_core118_packet176_20261101.py` validates1,296 direct original/C owned returns,1,152 separate original byte-helper returns and1,296 separate fill returns. It also freshly compiles the frozen104-byte caller and new176-byte callee together, observes640 connected caller returns and220 separately scoped callee returns including original counterparts. These connected returns add no second source count. The constructor remains a prefix with zero constructor-return credit.

The controls comprise48 metadata,23 direct policy and six native checks. Wrong C returns1,296 times and fails the independent model504 times;792 cases are explicit unchanged positives. A bounded scan finds six aligned ARM entry-call candidates and one exact-entry word, with no outside aligned ARM interior target in that scan. This is not a complete indirect/Thumb reachability proof. Data, helper, assembly and executable-extent credit remain zero.

## Overlay003 ARM 021DF6AC / 388

The new ordinary C routine matches all372 instruction bytes and16 generated pool bytes. Natural declaration order, local lifetimes and independent byte-array increments recover the native register and five-word call preparation without register forcing. Its names and resource/slot views are compatible measured labels rather than complete historical structure recovery.

`python match_ov003_panel652_20261101.py` runs72 pairs,144 actual entry returns,9,808 original getter/mapper/empty-constructor/cleanup returns,12,228 explicitly supplied service calls and three returning wrong-source controls. The actual ROM mapping function remains native. Resource/BSS state and other service behavior remain supplied test context; complete scene reachability and hardware behavior are unproved.

The tests observe324 of372 native code bytes. A48-byte inner tag127 block remains unsupported with the actual pure mapper and stable test slots: mapping127 to127 skips that block. All388 linked bytes still match, but no full-path gameplay-semantic claim follows from this byte comparison. The unobserved block, service boundaries and volatile/concurrent behavior remain unresolved.

All earlier source matches and current module checks must pass before this package becomes accepted. The exact-length original-object ROM remains scaffolding; a source-only ROM and full Windows/Android game remain separate unproved gates.
