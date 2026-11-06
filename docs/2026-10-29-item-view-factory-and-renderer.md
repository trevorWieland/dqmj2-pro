# Item view factory and renderer boundaries - 2026-10-29

The new ordinary-C hypotheses cover main ARM `0207571C..02075EB4` (1,944 bytes) and `02075EB4..020763CC` (1,304 bytes). They remain nonmatching and receive zero exact source credit. The adjacent96-byte function at `020763CC` has no source work in this batch. All identities refer to ROM SHA-256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`; no original inputs, application files or baseline files were edited.

## Frozen source and execution

| Native entry | Source/header | Hashes | Compiled/same-offset bytes | Evidence |
|---|---|---|---|---|
| main ARM `0207571C` | `nonmatching/save-core/20261029-preparation/item_view_factory_typed_20261029.c` and `item_view_factory_20261029.h` | source `8be365868e4c090d38a8decde515665295fca44122745bf4689b19b2693339d4`; header `4aac987ef4dba121f808c34bcfe9cb926bd5b7eac062703d1b49b0d93ec9b5ac` |1968/461|`evidence/application/item-view-factory-fixtures-20261029.json`, SHA-256 `07ac52d1b9dafff96914fbace361d33636e2f5974d741d0745eb95e4aa8d5f5e`|
| main ARM `02075EB4` | `nonmatching/save-core/20261029-preparation/item_view_renderer_typed_20261029.c` and `item_view_renderer_20261029.h` | source `f49226fb2398a7fd238731b220b665b4338fa04ee95dbdab5b7da69440c556de`; header `f4f514a8f8524b1bdbad95094fe2bc345a8e881f91e0326d6bed076efc9eedc8` |1344/241|`evidence/application/item-view-renderer-fixtures-20261029.json`, SHA-256 `089f6f10f98fe8417e0a8363214ea47fc11315f67aa07f6d38e5bb39d5b7f43c`|

Both use pinned2base O2 space. Source, object, linked hypothesis, native span and compiler hashes are in the reports. Each source/header is pinned before execution. Repository-independent replay uses the pinned Python executable with absolute paths to `evidence/application/item_view_factory_fixtures_20261029.py` or `item_view_renderer_fixtures_20261029.py`. Unrelated-working-directory replays passed. Full emitted hypotheses are used; native-sized truncation is not accepted. Their larger virtual footprints and declared downstream providers mean these are not source-closed module proofs.

## Factory findings

The factory passes263 contexts/534 actual returns. Mode3 covers all255 physical ItemTbl rows, independently checking the byte at context `021C5A24+7DA`. It clears both nibbles and applies descriptor conditions: byte+30 equal1 sets low nibble1, with kinds1/2 additionally setting high nibble1. Categories1/5/8/15 preserve that result; category2 sets low1 unless kind3; category14 sets low1 unless kind26; other categories set low1. These are measured layout/control conditions without an inferred universal targeting label.

Mode1 executes the actual owned-item list, append and predicate functions and checks page/count arguments for both sort modes. Mode6 executes the actual skill-count getter on normal, hole and full slot profiles, with the row count equal to that count plus one. Mode8 layout is separately bounded. UI/view/skill-list construction uses the report's explicit providers. Persistent state remains unchanged.

The native `02216260` call in mode3 has nine arguments. The initial m2c context discarded five stack arguments in its first call; the typed hypothesis supplies all nine. A selected-record pointer formerly loaded as one byte is recovered as a full word. Coordinate pairs are actual two-halfword arrays, rather than overflowing separate scalar locals.

Target-block bytes `021C6208..620F` remain sentinel-filled only under the declared downstream providers. This does not establish their behavior after full native rendering. Main `0207483C` executes original selected-item/quantity reads with formatting providers; it does not establish the earlier speculative "selection restore" name.

## Renderer findings and next dependency

The exact native extent is0x518, decimal1,304. An early decimal1,320 description was incorrect and was not used to draft or promote overlapping source. The renderer passes36 contexts/90 actual returns. Mode1 clears row flags before draw gating; mode6 clears them only with a nonzero draw byte; mode8 leaves them unchanged in tested contexts. Native quantity, slot and SkillTbl getters execute. UI formatting, invalidation and completion have explicit providers, and opaque return words reflect those providers.

Mode10 recursively dispatches through the prior mode. Tests cover prior modes0/1/3/6/8. Prior-mode10 recursion and malformed large signed-byte row counts remain unsupported, rather than accepted timeouts. The source reconstructs the observed64-byte local scratch buffer and coordinate pair without executable blobs or assembly.

Mode3 calls main `02074A54..020756E4` (3,216 bytes). This is the actual target-block writer: its body writes context+7E4, which is `021C6208`. Its eligible-record search calls the original overlay facade `02214068` with record/features/item arguments. The renderer fixture currently cuts that delegate explicitly; the next connected proof must execute the facade and native eligibility core originally. Existing sentinel findings remain provider-limited and are not borrowed as complete eligibility evidence.

The3216-byte dependency has a separate compileable hypothesis in `item_target_gate_typed_20261029.c` plus its header; it is not semantically adopted or exact-matched yet. The raw m2c draft's incoming saved-register placeholder and uninitialized temporary domains remain qualified. No fake register argument, forced register allocation, instruction patch or exact source credit is used to hide those questions.
