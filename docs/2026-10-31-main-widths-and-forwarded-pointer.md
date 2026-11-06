# Main-code width and pointer repairs

The current main frontier replay compiles 545 recorded profiles and produces linked images for 342 distinct unmatched functions covering 62,278 initialized bytes. Best linked images agree at 34,190 same-offset bytes; none of the initial drafts is a complete match. These are hypotheses, not accepted source coverage. Historical profiles and sources are hash-qualified against the measured ROM, processor, module, mode and configured boundaries before replay. The broader qualification contains 2,232 profiles; repeated profiles never multiply function or byte counts.

Four subsequent C repairs now genuinely match 284 bytes. Their native qualification is independent of eventual module/ROM acceptance. Each uses its separately demonstrated 2.0/base O2 inline-off profile. No register assignments, assembly, opcode edits or padding force bytes.

## Forwarded handle pointer

Main ARM 0203A1D4/140 must pass the incoming word pointer to original helper 0203A078. The old untyped C call overwrites R0 with the pointed-to value; original code loads that value into R3 while retaining the pointer in R0. An explicit pointer prototype and argument recover the complete match. Unsigned address arithmetic and unsigned left-shift input retain defined wrapped operations.

The helper clears an existing record's backlink and the incoming handle before checking a new slot. The slot stride is 372 bytes; availability is the full word at +12C. An active slot's priority comparison at +150 is signed. Successful attachment stores the new priority, sets flag bit0, writes the backlink at +14C and updates the handle. Synthetic aliasing includes a handle inside that backlink field.

There are 768 native/C recipe pairs: 1,536 top returns, 1,336 actual original helper returns and 1,730 supplied lower calls. Original detach24 and release152 execute. Five mutex, cleanup, callback and reset boundary identities are supplied without memory writes; complete scheduling/reset/cleanup semantics and ordinary scene reachability are unproven. All 136 caller instruction bytes and 4 literal bytes are checked. A whole-C omitted-pointer control genuinely links 140 bytes with two differing bytes; its 16 actual control returns contain rejection and positive cases.

Literal-pool addresses for the release helper are asserted against measured input bytes. Relevant registers, saved R3/R4-R11, SP, return mode, IRQ/FIQ control bits, full supported page images, data read/write events, ordered writes, call arguments and both stack canaries are checked.

## Byte offsets and word stores

Main ARM 02037D38/52 initializes the list header four bytes after a manager pointer. Main ARM 02037D6C/60 appends a new node to that same header. Their old signed-word-pointer expressions `arg0 + 4` incorrectly advance sixteen bytes. Explicit byte-pointer offsets fix the two complete units. The allocation initializer also receives the actual allocated pointer explicitly, preserving the existing machine argument contract.

Original list initialization and append helpers execute. The single allocator boundary supplies either a backed 20-byte node or null; no allocator implementation is claimed. Tests include empty/nonempty lists, raw heap words, allocation failure and wrapping halfword counts. The initialization trampoline is counted as a logical entry rather than a second physical return from its tail target.

Main ARM 02037750/32 clears full words at 020F1EC8 and 020F1F10 and returns the latter address. The old byte-array declaration caused a byte store at the second address. An explicit word store fixes the final differing instruction. Native execution checks all 24 instruction bytes; genuine linking checks the 8 literal bytes.

These three units pass 864 recipe pairs, 1,728 top returns and 3,264 physical native helper returns. Three wrong-C width/scale controls genuinely link executable images with one differing byte each and produce 72 actual control returns. Complete page images and ordered writes distinguish the errors. No ordinary allocator, scene, complete Windows game or Android execution is inferred.

## Reproduction

Run `python replay_root_main_profiles_20261031.py` for the frozen frontier inputs. Run `python match_main_reservation_pointer_20261031.py` and `python match_main_field_widths_20261031.py` for native qualification and whole-C controls. The matching reports retain source, object, ELF, LCF, compiler and helper binding evidence. The frontier/profile reports retain zero source credit. Integration must separately preserve earlier selections and pass all affected modules and the exact scaffold-assisted ROM build.
