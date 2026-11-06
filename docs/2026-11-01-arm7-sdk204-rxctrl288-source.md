# ARM7 receive initializer, 2026-11-01

Host ARM7 WRAM ARM037FB1E0..037FB300 now has a complete47-line ordinary C reconstruction. Fresh pinned base2.0 O4,p/IPA file/inline on,noauto compilation and genuine MWLD linking reproduce all288 bytes:248 code and40 generated literal bytes. The four frozen counter504 declaration headers are unchanged and resolve through the source-parent include path. No scratch output is an input.

Run `python validate_arm7_sdk204_rxctrl288_20261101.py`. The standalone validator regenerates source-only objects, genuine links, native fixtures, wrong-C controls and products before validating them. Its cold run from an unrelated directory and empty dedicated WORK reproduced the canonical report and all67 controls byte for byte.

There are72 original/fresh-C pairs:144 actual initializer returns,144 separately observed native28-byte clear returns,144 original descriptor-prefix fill returns,144 actual native mode-setter returns and288 actual mode-setter helper returns. Full-constructor return credit is0. No provider is substituted.

The original mode setter ARM027E8F3C runs after the original incoming descriptor prefix and0x694-byte clear. Its actual power/active-zone helpers remain. It returns0 and writes the selected mode to Config+32E and Work+350. Every supported mode0,1,2,3 is therefore produced by executed native code rather than a PC or branch override. Native mode callbacks and helpers receive zero source credit.

The independent model seeds all80 RX_CTRL bytes and verifies their actual complete word-clear at context+4DC. It then verifies36 ordered nonstack writes, every affected receive/global field and mapped WiFi halfword, all untouched nonstack memory, raw CPU/CPSR/stack and ordered reads/writes. The modeled receive starts are794/10C4/BFC/794hex; pool end is1F60hex. Receive cursor is at+4E0 and receive size at+3DE. The compiler independently verifies the complete WL_MAN size694hex, RX_CTRL size80decimal and all field/primitive offsets.

The actual clear helper is ARM037FDFD0/28. Its incoming words are0,destination=context+4DC,size80. A first diagnostic draft incorrectly encoded037FE014 in its source label while its explicit diagnostic binding still pointed to037FDFD0. Those historical bytes are preserved with zero credit. The final source label, ordinary linker address check, actual incoming ABI and executed28-byte helper all agree on037FDFD0. There is no helper/source-assembly credit.

The C API is void(void). Raw incidental R0 ends at04805F70 and is compared as machine state. It is not exposed as a C return value.

Global Work.Mode0..3 is a required source contract. The historical SDK C leaves its cursor uninitialized outside those values; the corresponding original fallback branch037FB22C is excluded from supported execution and has zero path/return/portability credit.61 of62 own instructions are exercised across all four supported branches. No source execution with undefined cursor is claimed. The report and caller-specific policy explicitly pin this limit, the actual original mode producer and the fresh native-model body.

Two freshly compiled wrong-C variants each return72 times and are rejected72 times: shortening the actual clear by4 bytes, and changing the receive pool end1F60 to1F64. There are33 metadata/product,26 direct caller/linker/producer and8 native-prerequisite controls. Missing/changed products, false source claims, wrong identity/declarations/domain, runtime-word corruption, instruction exhaustion and changed original modules are rejected. Modes4/FFFF are rejected before source-domain execution; those checks are not native malformed-mode success.

The absolute runtime word0380FFF4 remains tied to its measured incoming-descriptor origin. The adapter is limited to this complete caller/source/header/compiler/module/producer identity, preserves neighboring/default refusals and restores the frozen linker after success/error. Its nativeSymbols values are hexadecimal strings. There is no global data/namespace guard change, original-data credit or initialized-denominator increase.

Reference ordinary bodies come from ntrtwl/NitroSDK revisionccbbcc8b6db4c4dbba3d503d2026978d78977840. Raw hashes and independent Git blob identities are recorded. SDK revision equivalence, CC0 licensing and original assembly authorship remain unproved. All provisional stdio/stdarg/va_list parse shims are absent from final compiler inputs.

WiFi memory is statically mapped in the fixture. Physical bus behavior, concurrency and real scene/network reachability remain unproved. This is function-level evidence pending integrator whole-module acceptance. The separate bulk queue has29 closed/genuinely linked ranges4788B; its compatible named-word variant has20 exact ranges3812B, all unaccepted until their individual source/native gates pass.
