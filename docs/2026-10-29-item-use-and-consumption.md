# Exact item-use caller and consumption effects - 2026-10-29

## Source identity and reproduction

`src/mechanics_save/20261029_item_use.c` reconstructs main:ARM `020731AC-02073574`, 968 bytes, from the authoritative private ROM SHA-256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`. Source SHA-256 is `849de3cb78fb97c312c93443b0eb452c22b4857880c6f164c0f4e85565b69c1b`. The complete real-linked body equals native span SHA-256 `01f4edf468380c1caeac2e4560d63bc39b778c5d138ef5eee3a209fa91562464`.

The pinned MW 2.0/base compiler with recorded ABI flags and O2/speed produces the match. The source caches a pointer to the selected-index word, uses a full-width multi-target counter, and narrows that counter only for the feature-buffer call. Native code has the narrowing at that call and no byte mask after increment. The preserved byte-counter hypothesis had an extra mask and a narrower compiled extent. Natural switch case ordering resolved the final two message constants' register allocation. No assembly, opcode substitution or executable byte array is used.

Run `python match_mechanics_save_20261029_item_use.py`, optionally passing a repository-relative `--source`. It invokes `evidence/application/item_use_exact_fixtures_20261029.py` and emits `evidence/matches/mechanics-save-20261029-item-use.json`. Source, object, pinned real-link artifacts, exact own alias and qualified function/BSS dependencies are checked. The worker performs no registration; module/full-ROM acceptance remains the coordinator's gate.

The prior 964-byte typed hypothesis `nonmatching/save-core/20261029-preparation/item_use_globals_07.c`, source SHA-256 `52d578c54e4198496c05abd3266de1300dae6720b97db92ac6e3e4fbf27f568a`, remains frozen with its separate report. Its 1946 cases and 3922 actual returns are semantic evidence with zero exact source credit. That earlier harness rejects execution or data reads from the four remaining original bytes, ensuring its compiled source does not silently borrow an original tail. The promoted exact source has the full 968-byte extent.

## Native inputs and caller ordering

The function takes no explicit arguments. It reads signed item ID at RAM `021C61FC`, selected-index word `021C5B20`, target-record pointers at `021C6210 + index*4`, and the low nibble at `021C61FE`. Single-target mode uses the selected record. The other target modes remain runtime-unsupported by these fixtures despite the complete byte match.

Measured outputs include message-code byte `021C61FB`, core result word `021C6204`, and selected-record pointer `021C5DF0`. These are native fields and codes; no text or user-facing meaning is inferred for each message code.

For ordinary single-target items, native overlay0 feature mapper `02215D94` supplies the feature pointer, and wrapper `022140C0` invokes the original 1812-byte effect core `02066358` with eligibility enforcement enabled. A core return word other than full-word -1 produces caller success 1. The stored effect word can be zero or another value; it is distinct from the caller's success code. The original eligibility predicate may clamp over-max current resource halfwords before rejection, so caller return 0 can still accompany those modeled repairs.

The feature mapper is measured as a 100-byte stride with a +0x20 feature offset. Selected index 0 maps to RAM `0224577C`. The tested 64-byte feature region is deliberately zeroed. Native 12-byte getter `02215698` returns its static object address, and the native 24-byte mapper and 96-byte wrapper execute unchanged in nonbook cases. These native regions are scaffolding dependencies and receive no new source credit here.

For kind-26 books, duplicate and capacity checks precede the slot writer. Duplicate returns 0 and full capacity returns 2. Successful ordinary, zero-quantity and compacted-hole contexts return 1. The earlier measured book vector family is reused; its 26 physical book rows and five contexts are re-executed against both original and exact caller C.

## Consumption and persistent effects

A success calls native `02065DEC`, which tests ItemTbl byte 0x25 against a fresh native `RNG(100)` draw using strict greater-than. Effect RNG draws occur first; the consumption draw follows. A true decision calls native `020630E4(item,-1)`. The caller supplies no local owned-quantity gate in the tested contexts. With zero quantity, a successful effect can still be applied while the count adjustment clamps at zero. Ordinary menu access and upstream legality remain separate prerequisites.

The count helper's native effect includes an eight-bit count update, signed comparison against item-specific byte-0x27 capacity, a zero floor, and the call to already matched `02063810`. Consequently, consumption can affect more than the quantity byte.

`02063810` reads an item bit at RAM `021C0C44`. If initially clear, it invokes native recent insertion `02063860`, sets the bit, and returns the previous bit. Insertion selects one of two families by `(ItemTbl byte 0x2C == 7)`, each with a 12-byte stride at `021C0C64`. It writes the item first, retains nonzero values from the previous first nine entries, clears/compacts the ten-entry region and leaves each family's final two bytes untouched. No deduplication is inferred. The bit and queue changes can occur after a zero-quantity consumption attempt; neither field establishes current ownership by itself.

Relative to the native main-state deserializer mapping, quantity bytes begin at serialized bank offset 0xCC, the 32-byte item-bit region at 0x37B8, and the two 12-byte queue regions at 0x37D8. These are offsets within each physical bank representation. The tests do not select an ordinary active bank or add semantic partition coverage merely by naming raw fields.

The independent model initially omitted the observation/queue side effects and failed on physical item 25, kind 18, quantity 0. `evidence/application/item-use-model-revision-20261029.json` preserves that failed model scope. The model was corrected after inspecting the already frozen native count/setter/insertion/compactor chain. Accepted source and original inputs were unchanged.

## Execution evidence and limits

The exact source verifier passes 1946 cases: 1816 nonbook cases from 227 measured physical ItemTbl rows, four resource profiles and quantity 0/2, plus 130 reused book cases. There are 3892 actual routine returns and 30 original native leaf controls, totaling 3922. Every engine case receives fresh machine state, bounded execution, actual-return, stack-balance and preserved-register checks.

An independent complete saved-region/RNG model checks effect outcomes, eligibility clamps, consumption ordering, item-specific count clamping, observation bits, queue insertion and zero-count effects. Native and exact caller C also agree on transient memory, writes, UI events and hardware-division transactions. The book cases retain their native duplicate/capacity/slot/quantity/gold checks and compare meaningful native/source call traces.

Four UI/notification providers are declared for the nonbook generator; only the applicable boundaries execute in each case. The reused book generator declares five boundaries, including the derived-cache rebuild qualified below. Native inventory, predicate, effect, RNG, count, slot writer, observation and queue routines execute unchanged. Bounded nonnegative64-bit / positive32-bit hardware division is the only modeled device.

The suppressed overlay0:ARM `02215BC8` boundary rebuilds six target-feature cache entries; it is a functional derived-state boundary. The preserved book fixtures supply zero features and do not certify this rebuild or later derived-cache effects. The separate native cache proof in `2026-10-29-native-target-cache-boundary.md` executes the rebuild without callee providers; it does not retroactively broaden the book fixture scope.

The tested context is single-target mode, species 1, variant 0, zero optional bonus and zero native-mapped features. All three scene-specific kind-24 rows are excluded from the nonbook set. Physical reserved table rows are included without implying usable-item legality. Other target modes, live entities, nonzero bonus/features, kind-24 transitions, arbitrary record layouts, ordinary menu access and upstream ownership checks remain unsupported by runtime fixtures. Full byte equality and those runtime limits are reported independently.

BSS aliases `data_021c5a24`, `data_021c5b20`, `data_021c6124`, and `data_021c6210` are validated against the measured module configuration and exported with data mode. They receive no ROM-content hash or reconstructed-data credit. The baseline, application, original ROM/save and all earlier accepted source remain unchanged.
