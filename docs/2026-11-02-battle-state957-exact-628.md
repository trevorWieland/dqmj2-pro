# Battle-state957: exact628-byte ordinary C

ROM `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`, ARM9, overlay1, ARM `0x021E00B4`, span628 bytes. The preferred source is `src/overlays/ov001_20261102_battle_state951/source.c`. All628 bytes match through actual pinned compiler and MWLD linking, including616 observed instruction bytes and12 relocated literal bytes. Acceptance remains integrator-owned; no callee/module/ROM source credit is claimed here.

Two ordinary repairs recovered it. The historical844 draft interpreted the native word table at `0x02238950` as u8 loads at index*4; eight original LDR sites instead load32-bit actor words. A u32 table view fixes those reads. Its632-byte result remained nonmatching. Reversing the equivalent final DDA80 if/else exposes the original conditional stores and yields628 identical bytes, without assembly, byte patches, padding, forced registers or compiler permutations. Both earlier variants are preserved.

The preferred typed context aligns pointer facades with the existing selected DB8D0/D7E80 C views, and EEC7C's signed result/actor-pointer view; signed handle/frame inputs remain explicit. These declarations are not treated as independent complete original ABI proof. Actual caller words are tested. The first947 context and its540-pair proof remain historical; only954/951 is proposed for admission. The stronger952 corpus includes actual actor byte0xFF dereferences which null-actor filtering excluded from the first corpus.

Preferred proof954 passes542 original/C pairs,1,084 proper top returns and222 supplied service calls. Every raw signed phase-byte representation at context `0x022388EC+0x29` is exercised. The signed index at +0x28 is supplied as0/5/12; its incremented lookup remains within a supplied14-word table window, not an inferred legal actor count. Byte actor+0x31E is tested at0/255. Context +0x44 is a raw32-bit service handle; +0x08 receives raw0x1C or0x36. No semantic battle/state names are inferred from these values.

All GPRs,CPSR,8MiB RAM including stack, ordered writes, raw R0..R3 service words and proper-return opcode/SP/callee-saved state agree. A separate state/call/complete nonstack-RAM model passes. Services legally clobber caller-saved registers and NZCV with no supplied memory effects. No actual lower native service/RNG is counted. Three whole wrong-C images genuinely link at private nonoverlapping origins and actually return542 times each: wrong return rejects542, actor-word truncation rejects4, condition inversion rejects8. Remaining inactive-path positives are retained, not counted as failures.

Phase0 checks null actor words. Phase5/10 actually dereference actor+0x31E and require nonnull actors in this corpus. Phase8 only forwards supplied words to provided services. These are bounded execution prerequisites, not application restrictions or proof of ordinary scene validity. Full lower service consumption/formal arity, UI/resource/handle lifecycle, actor eligibility meaning, record-byte33, persistence and caller reachability remain unproved.

Reproduction:

- `python -I -S match_ov001_battle_state954_20261102.py`
- `python -I -S qualify_ov001_battle_state955_language_20261102.py`

Absolute script paths also replay from a different working directory; report and deterministic gzip hashes match. Explicit C99 and compiler-default profiles produce identical complete linked bytes and original relocation types/addends/encoded words. Prior source files, application code and shared registries are untouched. The companion624-byte state956 hypothesis is separate pending work and is excluded from this handoff.
