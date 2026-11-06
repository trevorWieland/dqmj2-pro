# Complete native-record capacity decision — 2026-10-30

World SCR entry 279, code-relative `[0,544)`, now rebuilds from one ordinary C
definition, `src/scripts/20261030/batch21/evaluate_record_capacity.c`. Modes 0, 1,
and 2 query the native count and return binary32 1 when it reaches thresholds 1,
2, and 3 respectively; otherwise they return 0. All other measured modes skip the
query and return 0. This is 544 bytes of qualified interpreted-source credit,
with zero new native bytes, complete images, padding, or whole-ROM source credit.

The named getter binds SYS187 to original main:ARM02052DBC. Its five original
counter calls are retained: ARM020629E0 once, then ARM02062AA0/02062AD0 twice each.
The first counts nonzero words at `+14` in 100 records beginning `021BD674`, stride
`84`. The two secondary counters consult three UID entries at `021BD540` and
`021BD54C`, through the real full-word UID lookup ARM02062A10. In the measured
stable state the handler arithmetic produces 100 minus the first count. It was
not replaced by that algebraic simplification, and atomicity during concurrent
ARM7/state changes is not claimed.

The synthetic corpus includes 0, 97, 98, 99, and 100 physically occupied UID-word
records. UID words include `80000000`, `12345678`, `FFFFFFFF`, and 1. A separate
alias context has one occupied physical record and repeats its full `80000000`
UID in all three entries of both secondary arrays. The real secondary counters
return 3/3 while the final query still returns 99. Twelve actual full-width lookup
arguments and five actual nested counter returns are observed per query. This
proves the measured arithmetic and word-count behavior; duplicate UID scenarios
are synthetic and do not establish valid records, party legality, ownership,
save import restrictions, or ordinary gameplay reachability.

The C source explicitly names raw VM argument word 0 and module slots 0–2. The
current encoded audit finds no outside references to those three slots; opaque
native/computed references are not exhausted, so they remain conservative extern
module objects. The mode is copied before the query clobbers argument word 0.
The sampled-count slot is preserved when no query executes. All other 253 slots
and persistent bytes must remain unchanged. The complete range has one public
root, one private return at 540, no public interior root/direct outside interior
transfer/shared return, and excludes following padding `[544,552)`.

The new restricted backend v17 imports the frozen v16 compiler dependency, adds
only the named no-argument count query, scalar less-or-equal decisions, and final
float return needed here. It makes no general C compiler claim. Six isolated
source-only inputs are sufficient: core parser, v16 dependency, v17, C, header,
and symbolic object profile. Original bytecode is not a compiler input. The emitted
544-byte range hashes to
`01d3a853941492178b83c3b86d9200d2582530213318ceded1602d1cdd02f415`
and reproduces the original decoded image when inserted.

There are 26 profiles and four threads, two serialized calls per fresh context,
and two implementations: 416 complete own-entry executions, 6,808 actual native
returns, and 1,520 separately observed nested counter returns. Every own record
executes, with both outcomes at all six conditional sites. The raw input controls
include negative zero, unmatched integers, positive/negative infinity, quiet and
signaling NaNs, and a positive subnormal. No provider, native stub, executable
patch, PC override, or source-callee credit is used. Native bounds remain 20,000
instructions and 1,000,000 microseconds per call, with a 40-record script cap.

The differential evidence compares general registers/CPSR, ordered native CPU
stores, full VM state, persistent bytes, all register slots, ordered module writes,
raw results, all counter returns, and full UID arguments. The independent accessor
reconstructs the record corpus, scalar branches, query and return values, exact
slot effects, and all complete traces, then freshly rebuilds source in isolation.
It qualifies every compiler object-access PC against the current decoded image.
Ten malformed source/type/namespace/storage cases fail before output. The registry
adapter rejects 22 mutations before accepting the one positive unit. Root and
parent-directory invocations pass with identical verification output.

Reproduce full source/native evidence:

```powershell
& 'C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe' 'C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\match_scr_record_capacity_20261030_batch21.py'
```

Replay current source-only acceptance and mutation controls:

```powershell
& 'C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe' 'C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\verify_interpreted_record_capacity_sources.py'
```

Frozen identities:

- Backend `42258e63e255eda2ddbd21d473c613109bcd9f38dfe526a29613c5e41af761a7`;
  matcher `e046f4aa2eb4d33f0990725b8c92f11f8ecc250b4be119391eab27c84aa687de`;
  fixture `5334092f9383c57f44eb3989326230ce7c1c745d902217de1ec01e1e925ecafd`.
- Report `evidence/matches/scripts-20261030-record-capacity.json`:
  `d6d155ec158b98c26ab929c0dad548a0a2c67443bf14e7c332a33e35d64e0b76`.
- Accessor `5e814a03f79480267be48b9b7ece68d02693141db73ae1931edff5c3d74696ba`;
  adapter `831b04780a08873487111e0ca70ff7ec9afdeb7c52b1aef482d7957296a67d36`;
  mutation suite `2972e711151ce7f3b84e4d76b0b983758835c0869c0fcb352de4efd7823104a7`.
- Verification `evidence/verification/interpreted-record-capacity-source-negatives-20261030.json`:
  `1af48e9c7e9a0824a6a56fa85432ee0eac8d25989b658d35dbc0842be8460aed`.

All current source/include/profile hashes and native-root provenance are pinned
in the report. The integrator owns registry acceptance. Earlier frozen files,
original inputs, application adapters, the baseline, and shared ledgers remain
unchanged. The routine is not a complete admission, acquisition, or import policy;
its callers and further state constraints remain separate work.
