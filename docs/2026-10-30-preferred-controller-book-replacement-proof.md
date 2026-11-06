# Preferred controller book-replacement proof

The existing ordinary-C hypothesis for main ARM`020735F8..020743F8` now reproduces the full native book-replacement scenarios. It remains nonmatching: the native function is3584 bytes and its compiled hypothesis is3604 bytes. Source coverage stays zero. No earlier hypothesis, accepted source, generator or original input was changed.

`evidence/application/book_replacement_flow_preferred_20261030.py` rebuilds the frozen preferred source `nonmatching/save-core/20261029-preparation/item_control_explicit_arguments_20261029.c`, SHA-256 `6b0d3493b87e1b7c4ae21318a3db444035906d5445dbf002c07817d9b7556805`, with header SHA-256 `6d676e2e9beaa2eb605b267bbcdbe3cac74916220f687397d5ace023f87ec8e9`. It uses the pinned MW2.0/base O2/space compiler and actual MW linking; compiled object SHA-256 is `57be4a52146dc9b8e901eef372d6fa59cfcef5e113616452439143fca70f441c`. The real-link mismatch is retained rather than treated as source acceptance.

The new report `evidence/application/book-replacement-flow-preferred-20261030.json` has SHA-256 `18541df5ab51f1d4768594fd8b0f157b6fc77bbc0d06e1c2cc0f3b36901e53fd`. Its native golden reference remains the frozen `book-replacement-flow-20261030.json`, SHA-256 `3b9c1badd9a1beb285b2d0735ab1ab9da6872ec0cc93d400bd31bcfe6f766679`. Normal and unrelated-working-directory replays of the new script produce the identical new report hash.

There are eight synthetic profiles: four full-capacity species1 replacements for quantity1/2 and first/last selected old skill, plus duplicate-skill and nonzero record+`0x33` negative profiles at each quantity. Book48 learns skill137 and has consumption threshold100. The source controller returns32 times; original native setup functions return40 times. These72 actual host returns are separate from the old golden report's72 returns. Nested calls are not added to those host counts.

For each profile, the new script checks saved-byte changes and saved-state hashes against the original golden result, plus the resulting slot bytes, quantity, state, previous state, phase word, normalized native slot/library/chance/inventory calls and explicit provider arguments. Every one of the32 source-controller frames also happens to reproduce the original ordered non-stack write trace exactly; that is measured in the report rather than assumed from semantic equality.

The successful path follows states3→9→5→9→6→7→8→9. The existing native use caller returns its full-capacity path without debit. An explicit modeled user choice then selects an old skill slot; native slot initialization writes learned skill137 with allocated0, native library update runs, and native chance/inventory consume one book. Quantity1 moves to phase4; quantity2 moves to phase2. Duplicate and record-byte blocked profiles never call that mutation chain and leave the saved region unchanged. The unnamed record byte is offset`0x33` hexadecimal, decimal51.

Only the controller is patched with compiled hypothesis bytes. The target writer, factory, use caller, slot setter, library, RNG/chance, inventory adjustment and derived-cache routines execute original instructions. Display, widget count/page construction, text descriptors, cursor movement and scene-refresh boundaries retain the explicit synthetic providers documented in [the native replacement writeup](2026-10-30-native-item-targets-and-book-replacement.md). Those providers limit scene/UI reachability claims and broader side effects.

Because the compiled controller extends20 bytes beyond its native span, the adjacent original entry`020743F8` is explicitly trapped. None of these supported scenarios reaches that overwritten function. This qualification prevents the source experiment from treating overwritten adjacent code as an original dependency. It is not a legal module replacement or evidence for other paths.

Reproduce with Python3.13.5 and Unicorn2.1.4:

```text
python evidence/application/book_replacement_flow_preferred_20261030.py
```

The generator rebuilds into its own `work/mechanics-save/20261030-controller-book` directory, pins source/header and native golden hashes, records replay dependencies, requires bounded actual returns and preserves original native IDs/record data. Ordinary menu entry, other books/species, canceled confirmations and complete engine scene effects remain unproved. This proof strengthens the unchanged preferred hypothesis without increasing exact bytes or freezing out later matching recovery.
