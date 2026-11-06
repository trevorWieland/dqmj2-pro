# Complete module-global sentinel initializer — 2026-10-30

World SCR entry 256, code-relative range `[552,1048)`, now rebuilds its complete
496 bytes from `src/scripts/20261030/batch18/clear_registered_keys.c`. The sole
ordinary C definition assigns -1 to ten named key globals and ten named flag-index
globals. This is initialization-only source, with no conditional decision-logic
claim. Native byte credit, complete-image credit, and whole-ROM source-match credit
are zero. The following eight bytes `[1048,1056)` are excluded as padding.

This is the actual encoded initializer for the twenty globals read by entry 259
([the preceding source proof](2026-10-30-scr-registered-primary-float-return-batch17.md)).
The shared module slots are 3–22, with no private local slots. The current encoded
reference scan finds two writes and one read for each: one write here, one in the
registration flow, and one read in entry 259. No natural initializer/registration
caller path or whole-program global domain is proven. In a port, these globals
belong to the VM/module context; their C spelling does not authorize sharing state
across independent game instances.

The range has one public root, one private return at 1044, one initial unconditional
branch, and twenty ordered stores. No external direct interior transfer, public
interior entry, or shared return is present in the current encoded audit. Opaque
native and computed references remain unresolved. No copied-data declaration,
byte array, original opcode transcript, or source PC is used as authored C.

The separate `scr_c_compiler_20261030_v15.py` backend parses a bounded void C
definition, an explicit header of extern float objects, and named constant
assignments. It emits each binary32 assignment and the implicit private return.
It accepts only exactly representable integer constants in the supported bound;
arbitrary float expressions, global-to-global copying, calls, and general C are
not supported. It does not modify or import the earlier v14 backend.

The source-only directory contains only five compiler inputs: pinned core parser,
new backend, C, header, and symbolic global binding profile. No original bytecode
is supplied to the compiler. Its 496-byte emitted body equals the original range,
and the image rebuilt by replacing that range equals the original decoded image.
The same original ROM/archive/member/code identities as batch 17 apply. The ROM
SHA256 remains `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`.
The initializer body hashes to
`1d5bf894571372060fd1d47736038dc1ed2e5049864f8cf53180749bace24ff8`.

Independent original-versus-recompiled execution uses eight initial register-file
patterns and all four VM threads. The patterns preserve raw random bits, zero,
`FFFFFFFF`, -1, quiet/signaling NaNs, alternating infinities, and signed zeros.
Each fresh context executes the complete initializer twice through native
start/fork/reentry functions. Across both implementations this is 128 complete
own-entry executions and 3,104 actual native returns. The larger return count
includes initialization, forks, reentry, and interpreter calls, and is not a
script-function count.

The fixture observes all twenty aligned four-byte module-global stores in order,
all 236 other VM slots, the unchanged argument bank, all persistent bytes, native
general registers/CPSR, ordered CPU-store hashes, and full VM context. Every own
record executes and actually returns. There are no providers, native stubs, or
unsupported-path successes. The native cap remains 20,000 instructions and
1,000,000 microseconds per call; the SCR cap is 22 records. The separate count-only
research experiment was not adopted for this proof.

Ten source/type/storage controls reject an undeclared assignment, inexact constant,
unknown constant object, unsupported global copy, second definition, shadowed
function, aliased slot, out-of-bank slot, duplicate declaration, and wrong type.
The standalone accessor validates current original input hashes, source products,
direct/global boundaries, source-only re-emission, complete returns, ordered writes,
and all per-unit accounting. Its adapter suite passes 22 meaningful mutation
rejections plus the positive unit. Root-directory and parent-directory runs both
pass and produce identical verification output. Missing products withhold credit.

Reproduce the full native proof:

```powershell
& 'C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe' 'C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\match_scr_registered_initializer_20261030_batch18.py'
```

Replay source-only acceptance and mutation controls:

```powershell
& 'C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe' 'C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\verify_interpreted_registered_initializer_sources.py'
```

Frozen identities:

- Source `a80a041d1dba20b5af22076d74a46d7e0049b6884a00f2fe23b601f3761ffa07`;
  header `dd27c117fd18c582c31082f553b742b1552f96e3cdc46041a4d8d95f41bc1644`;
  profile `35b6f75a7230c6dd47a9c2d0a461fd90585d8b92b13e23390ce17eded0487cd3`.
- Backend `248acc6d862852666789be94e73bdc5b35ffcf822d08ca7e1398e9db24783318`;
  matcher `d797fafe52ee93d09628445d7d1e0d68ac348edb8f8de624d192ab913815ace1`.
- Report `evidence/matches/scripts-20261030-registered-initializer.json`:
  `6114010b90e93951b5305632072c3eba997d384fd7e6306e0779677aac105f7f`.
- Accessor `9e450b2a001d9572d45ef246948a669b83099c49db69f38a30114a6d762d7672`;
  adapter `365e6c3eb11fcb41bd32984a6b49cf1c9875e31530a5dad3d3672c3490f27d41`;
  mutation suite `d357d511340f899ccfb34b012f0b47686ba423d872a240ac43e583f95fc95287`.
- Verification `evidence/verification/interpreted-registered-initializer-source-negatives-20261030.json`:
  `733ea27036e47b9a50253e44d3cf1920d7c91c5e1a7a61b307db5f792bf90ea0`.

The integrator owns registration. These new files do not change shared registries,
ledgers, application adapters, original inputs, the baseline, or prior frozen
source/proofs. Registration logic, inferred gameplay meanings, opaque program
closure, and full-image reconstruction remain open.
