# Battle phase965: exact624-byte ordinary C and original byte-getter chain

This packet reconstructs ROM `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`, ARM9, overlay1, ARM `0x021F9B54`,624 bytes. Preferred source959 genuinely matches all624 bytes, including616 observed instruction bytes and8 relocated literal bytes. It remains pending integrator admission; no native callee/module/ROM credit is claimed.

The previous844 draft had a missing condition on its default branch. Original native code increments the phase only below50; the draft incremented all other phases, incorrectly changing the phase55 counter path and inactive high phases. Adding the actual unsigned phase<50 guard produced604/624 bytes. Expressing each byte increment/store as the condition's ordinary assignment expression preserves the original truncated-byte comparison and scheduled byte store, yielding complete equality. Wide-temporary/direct-preincrement/inline/space alternatives are retained as failures. No register forcing, volatile, assembly, opcode patches or padding was introduced. The directory preincrement-debug was misnamed: its actual change was-inline on; -sym remained on. The erratum pins that original experiment without rewriting history.

Proof961 passes1,536 original/C pairs and3,072 proper top returns, with2,592 explicitly supplied service calls. Every raw phase at context `0x02239A14+0x03` is covered; every count at +0x00 is covered in phases0x28/0x37, and every raw flag at +0x04 is covered in phase0x24. Unsigned byte increments wrap before comparison. Ordered actor-byte writes at +0x324/+0x358, phase/count/flag writes and raw selector+0x0A=4 on the closing path are independently modeled. No ability, actor role or scene meaning is inferred.

The original main `0x02041800` wrapper and `0x020417F8` leaf execute for the actual predicate against1. They read raw u8 at `0x020F6100+0x02`, supplied as0/1/255. Across preferred original/C runs there are12 actual native physical BX returns and24 logical wrapper/leaf entries. The leaf at0x020417FC returns directly through the wrapper's LR; instrumentation suppresses a duplicate tail frame while recording both entries. These counts are separate, not added together or credited as new callee source. No RNG executes.

Complete GPR/CPSR/8MiB RAM including stack, raw service words, ordered writes and return opcode/SP/callee-saved state agree. An independent state/actor/call/complete nonstackRAM model passes. All616 own instruction bytes are observed. Three whole wrong-C images genuinely link at private nonoverlapping origins and properly return1,536 times each: wrong return rejects1,536; missing default-domain guard rejects874 with662 positives; wrong raw-byte predicate rejects2 with1,534 positives. Inactive-path positives remain explicit.

All other UI/resource/resolver services are supplied with legal caller-saved/NZCV clobbers and no memory effects. The actor is explicit writable0x400-byte synthetic storage. Resolver side/slot values are actual caller words, not proof of complete original formals or legal party membership. Original scene/caller initialization, UI/handle/resource lifecycle, eligibility meaning, record-byte33 and persistence remain unproved. The companion628-byte function957 is an independently frozen packet.

Replay:

- `python -I -S match_ov001_battle_phase961_20261102.py`
- `python -I -S qualify_ov001_battle_phase962_language_20261102.py`

Absolute script paths work from the alternate directory. Canonical/alternate report and deterministic gzip hashes agree. Compiler default and explicit C99 produce identical complete linked bytes and original relocation types/addends/encoded words. All accepted/shared/application files stay unchanged.
