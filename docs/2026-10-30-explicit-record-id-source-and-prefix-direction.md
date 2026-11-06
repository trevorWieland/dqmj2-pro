# Explicit record ID source and prefix direction

The three alternatives in `evidence/matches/mechanics-save-20261030-record-arguments.json` forward their real full-word record ID to a typed lookup. All 128 bytes match the measured native ARM spans after compilation and an actual pinned MW link. These spans were already accepted; the alternatives add zero functions and zero bytes. Integrator selection and complete module/ROM regression remain separate acceptance steps.

The namespace is the private 175,959,612-byte ROM with SHA-256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`. All functions below belong to ARM9 main in ARM mode. Compiler2.0/base SHA-256 `7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880` uses the report's complete O2/speed flags and the existing local license. The independently validated linker SHA-256 is `bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74`.

| Address and extent | Preferred source | Measured contract | Cases / actual returns |
| --- | --- | --- | --- |
| `02062ECC..02062EE4`,24B | `src/mechanics_save/20261030_record_skill_pointer.c` | `u8 *(u32 id, int slot)` returns lookup address +`0x7A`+2*slot, with no validity guard |529 /1058 |
| `02062E18..02062E44`,44B | `src/mechanics_save/20261030_record_header_write.c` | `int(u32 id, const void *input)` writes20 bytes from input into the found record prefix, then returns1; absent record returns0 |412 /824 |
| `020640B4..020640F0`,60B | `src/mechanics_save/20261030_record_descriptor_nibble.c` | `u32(u32 id)` reads species at record+`0x18` and returns bits4..7 from the low packed byte of EKT+4; zero/missing ID returns0 |806 /1612 |

The preferred sources have SHA-256 values, in table order:

- `9d10118d03b6bf6149bf7a47340afeaeb8ffc7aaf525e246abc82fa051950e1d`
- `d60d86ed28bf6e433afffbaa420e27b513adbbf8cb5f2ead897d1501c376ae43`
- `ebb3ce818c9a62293df60038b0ae36d89f201276274765c15d6a8ff34ff2243e`

Their compiled object hashes are, respectively:

- `b251e7e48cd4b6a3d7e628d1ecde50a1c09de67fc72199dcccbe4b0377c992c5`
- `a06059b0b39f5c791adbaa644580d929b5a80bfdbd3bf7c3ba1aeb0efd724e26`
- `5d94b17f8e2e27f12b22dff3da476c084a926cb4a60fbecd4ff0fb3e579eb5b2`

The native and genuinely linked body hashes are identical in each case:

- `1e610d76a1d155c09dd8d0bd9c8824e49152b0fd04cea9db7c3765389ca4d535`
- `1c765217fe57535e7c9450076bd484387072acb7c87581d52ad214e7f9c83301`
- `e1c570d3b57063b4ceb0ddd48d3990fa2ae97f4f9114cc8ee3968bec27b9d3ca`

Before authoring these alternatives, `ledger_state.collect_matches` confirmed the actual primaries were the retained runtime09 pointer and prefix functions and runtime05 descriptor function, without later selected alternatives. Their old source hashes are recorded under each migration proposal. Those files remain unchanged. Their omitted lookup argument relied on implicit native R0 retention; the replacements express the argument in C. The descriptor shift is explicitly unsigned before left shifting.

## Native effects and bounds

`02062A10` compares a nonzero full32-bit ID against the IDs at offset`0x14` of100 records starting at`021BD674`, stride`0x84`, and returns the first match. IDs are not array positions. Fixtures include all100 positions, high-word IDs including`FFFFFFFF`, absent IDs and duplicate first/last IDs. Zero is absent even if a stored ID were zero.

The skill-pointer helper preserves the original lack of bounds checking. Unsigned native-width integer address arithmetic avoids null-pointer arithmetic in C. Invalid returned addresses from missing IDs or extreme slots are compared as words and never dereferenced. This is not a safe host-pointer API for unchecked input; only valid records/slots support later dereference.

The prefix function is a setter. Original `02008E0C` takes source,destination,size: its arguments are `(input,record,20)`. A present record changes only its first20 bytes; the ID at+`0x14` and species at+`0x18` remain unchanged. Writable mapped non-overlapping input is tested at alignments0..3 with distinct byte patterns. For absent IDs the routine does not inspect input, including null input. Null or overlapping input for present IDs is unsupported.

The initial copy-out hypothesis was rejected by an independent native test before registration. Its generator and typed hypothesis remain under `evidence/attempts/record-argument-copyout-model-20261030.py` and `record-header-copyout-hypothesis-20261030.c`. The separate original-code direction control in `evidence/attempts/record-prefix-direction-control-20261030.json`, SHA-256 `21d9589d6b441b7964c948e038986be75443bf5fc426d7ef37d6a8e30e46b9d7`, records the prefix changing to input bytes while input stays invariant. Neither failed byte-matching hypothesis nor this control gains source coverage. A name/text interpretation of the20-byte prefix is not established here.

The descriptor proof covers all512 physical rows plus every nibble0..15 with varying unrelated low bits and high bytes. Its nibble receives no gameplay label. Negative/out-of-range species and corrupted lookup storage remain unsupported.

## Reproduction and measured reports

Run Python3.13.5 with Unicorn2.1.4:

```text
python match_mechanics_save_20261030_record_arguments.py
python evidence/application/record_prefix_direction_control_20261030.py
```

The matcher also accepts `--source-directory` as an explicit repository-relative directory containing the exact pinned source filenames and bytes. It rebuilds each source, verifies source/object/link hashes, compares all original bytes, requires the real linker exit0 and exact-caller validation, and produces native symbol identities and zero-credit primary migration proposals. It never edits registry or selection policy.

The canonical report SHA-256 is `351c6cfce196c11f89b070ade458213870661e45b35828010d6a11a31e9aefab`. Its separate fixture report SHA-256 is `9a8ace6f08c62e49504be239e390b6b6fd9734d529eb34b99718afcd5accba8a`. Normal and unrelated-working-directory replays produce those identical hashes.

There are1747 deterministic cases and3494 actual top-level native/compiled returns. Nested lookup, descriptor and copy returns are excluded from that host count. Each engine/case receives a fresh Unicorn machine, bounded instructions, initialized registers/stack and an actual return/SP/preserved-register gate. All original callees execute without providers. A complete independent saved-memory model permits only the found prefix write; input and descriptors stay invariant. This does not establish ordinary scene reachability, bank selection, prefix semantics or safety outside the stated domains.
