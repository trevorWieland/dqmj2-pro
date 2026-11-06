# Three connected consumed-input repairs

Three new ordinary-C bodies reproduce their complete measured ARM extents under genuine compiler and MWLD comparison. They are candidates for integrator acceptance; this lane performs no registry or shared-build mutation.

| Main address | Bytes | Reconstructed behavior |
|---|---:|---|
| `02040E74` | 316 | Tests three raw nonzero handle words and conditionally submits up to four requests; accumulates result bits 1/2/4 and sets descriptor halfword bit zero at offsets `10`, `20`, `32`. |
| `0205F920` | 108 | Reads a byte count at object `22`; obtains successive `90`-byte entries from object pointer `1C`; forwards each entry byte `81` into the native registry clear; releases the final nonnull buffer with both input words and clears object `1C`. |
| `02048E14` | 96 | Releases each nonnull object word at `4`, then `0`, through the original signed-selector thunk, then zero-fills exactly 100 bytes of the object with the original word-fill routine. |

Offsets and strides above are hexadecimal except the explicitly decimal 100-byte fill. Raw names do not assign gameplay roles, live ownership, public capacities or scene access.

## Measured source changes

The 316-byte function's native first and third request paths load their handle into R3. The old hypothesis supplied only three words to `0202ACEC`; the corrected interface passes all four words on every path. The actual lower routine saves incoming R3 and forwards it to `0203C4BC` when its signed queue limit permits a submission. The new source also retains bitwise result accumulation and uses defined unsigned word shifts for the native low-16-bit length encoding.

The 108-byte function's native cleanup loads the buffer into R1 before calling `0202A498`. The corrected source forwards that word explicitly. Its initial unsigned byte-count comparison uses the initialized loop index; this naturally reproduces the original unsigned condition code without assembly or instruction edits.

The 96-byte function similarly retains each loaded buffer word as the second `0204532C` argument. That original 12-byte thunk performs its actual BX through IP to `0202A498`; the proof validates the instruction, literal target and unchanged return link. It counts the tail continuation as one physical return rather than two.

Sources are under `src/mechanics_save/20261101_lane_measured_inputs/`. The exact profile records every source hash, original historical compiler path/hash and flag. All three use the pinned Metrowerks 2.0/base binary. The 316-byte unit retains its explicit speed option; the other two retain their different historical flag lists. No configuration is generalized from another unit.

## Connected native execution

`python match_mechanics_save_20261101_lane_measured_inputs.py` rebuilds all declared objects and linked bodies, runs the positive matrix and whole-C rejection controls, verifies source/native/link identities and publishes a canonical match report.

| Entry | Contexts | Original plus C returns | Other actual native returns | Supplied calls |
|---|---:|---:|---:|---:|
| `02040E74` | 1,920 | 3,840 | 10,320 | 16,768 |
| `0205F920` | 300 | 600 | 94,752 | 0 |
| `02048E14` | 3,072 | 6,144 | 13,856 | 0 |
| Total | 5,292 | 10,584 | 118,928 | 16,768 |

All own executable instructions are observed. Every run has a fresh machine, actual bounded return, empty call-frame stack, restored SP/callee-saved registers and control state, stack guards, full register/flag comparison, native/source read/write/call trace equality and independent full tracked-memory/return checks. Full per-case evidence is retained in deterministic gzip, not omitted after digesting.

For the 316-byte matrix, original `0202ACEC` executes its signed 16-bit capacity/count checks and stores; original `0203D348` executes its constant-zero return. Only mutex boundaries `0200708C`/`02007110` and submission `0203C4BC` are supplied. Provider arguments, raw outcomes, call edges and legal caller-register/flag clobbers are checked. This does not establish actual service completion, scheduling or the validity of supplied payload pointers.

The other two matrices use zero function providers. Original `0205F98C`, `0204861C`, `0204532C`, `0202A498`, `0202B4E8`, `0202AD78`, `0202ADA4`, `0202B1A8`, `0202ADFC`, `0202ADCC` and `02008C14` execute where reached. Synthetic manager records, allocation/free lists and payload headers exercise null/inactive/error branches, high-address input pointers, counter wrap and adjacent block coalescing. An independent list/range model checks all stored bytes and consumed input order. These disposable structures do not establish ordinary game heap initialization, live allocation validity or all allocator modes.

The byte-count cases include 0/1/2/3/7/127/128/254/255 with repeated and high byte registry keys. All 256 signed selector-byte encodings are covered in the object-clear matrix. Valid manager rows and invalid selector outcomes remain distinct. Synthetic registry group and backing extents are probe domains, not inferred import limits.

Three complete compiled wrong-C bodies alter a submitted fourth word, skip the first registry row, or omit the first release. All 24 original/wrong invocations actually return: six independent rejections and six causal positive controls. The fourth-word negatives have spare signed queue capacity and reach the submission boundary, avoiding an ignored-input path.

Two separate missing-backing controls require exactly `UC_ERR_READ_UNMAPPED`; neither receives return or post-fault credit. Unexpected timeouts and other errors fail the generator.

## Scope and retained research

No item consumption, saved-state mutation, preparation eligibility, ordinary scene access, bank choice, chronology or reduction of the 40,560 unknown save bytes follows from this runtime resource/registry evidence. The 108-byte source remains a void view with its physical R0 compared; the other raw return views do not establish original public declarations or all caller consumption.

The current-excluded historical-near sweep reproduced 12 units / 3,164 native bytes with the actual historical profiles. Complete original source hashes, object/link provenance and failed measurements remain in compact reports and compressed provenance sidecars. The separate 236-byte input-mask hypothesis remained nonmatching in this packet; later trials are separate work. Original hypotheses, prior accepted source and earlier oracles are preserved.

Canonical replay rebuilds every required object itself and reads no scratch golden or external working-directory file. Native symbol closure includes the exercised lower routines and the byte global at `02102970`; helper bytes receive no additional source credit. Integrator module/ROM acceptance remains a separate gate.
