# Numeric transition context producer and validation accessor, 2026-10-29

The previously isolated `s07e01.e` entry102 transition has a measured native input path and a real script caller. This extends the historical [352-byte source proof](2026-10-29-scr-numeric-transition-batch04.md), whose C/compiler/fixture/report remain frozen.

The raw byte at RAM `0x02102DC8` is read by main:ARM0205BE14 and written by main:ARM0205BDFC. The latter stores its argument's low eight bits and returns the previous byte. The original overlay000 launcher ARM021E4E9C, when starting entry129, calls this getter at ARM021E4F7C, converts its unsigned result to binary32 at ARM021E4F80 using main02025A70, and stores that word into VM context `0x02233AE8+0x450` at ARM021E4F88. This bank value is not a source function parameter passed on the SCR call stack.

Entry129 starts at SCR137336, captures context0 at137348, runs original SYS100 at137372 and captures its separate result at137380. Its CALL at137404 then enters the complete reconstructed routine at64612. The callee independently reads context0, numeric0 and numeric9. The real CALL increments depth0 to1 and pushes continuation137416; the callee's private RET at64960 restores depth0 and resumes137416. Static entry/direct-call reconciliation finds entry102 as the callee's sole table alias and this one known direct script CALL, with no decoded external interior entry. Computed or opaque alternate entry coverage remains incomplete.

Thirty fresh native scenarios pass **649 actual bounded returns**. The suite varies raw59/60/61, numeric0=6/7 and numeric9=1/2 with independent seeds, plus low-byte boundaries0/255/256/316/0xFFFFFFFF. Raw316 becomes60 through the real setter/getter/import path and satisfies the context predicate. The complete callee changes numeric9 from2 to3 exactly when imported context0=60 and numeric0=7. Every other persistent byte remains unchanged.

The launcher import is demonstrated with deterministic synthetic native input supplied through the original setter. Neither upstream ordinary event selection nor a real scene producing raw60 is proved. Qualified relocation/parent/BL indexes list seven direct setter references and sixteen direct launcher references across separate measured modules; their existence alone does not execute or validate those upstream callers.

The entry129 runs stop at continuation137416 after the complete callee returns. This is an explicit supported outer boundary, **not outer-script termination**. A separate native launcher call with entry102 starts that valid table entry but returns0 from the launcher's unsupported switch case and does not populate context0. After initialization, this direct-entry context remains0; the complete callee consequently returns without the transition. Direct table validity and successful native launcher handling are distinct observations.

```text
python C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\evidence\encounter\numeric_transition_producer_20261029.py
```

The fresh replay passes from the parent DQM directory. Every counted native call reaches its sentinel within20,000 instructions and one second, preserving SP/R4-R11. Ordered stores, register/CPSR/state hashes and full persistent-state expectations are retained per scenario. The report assigns zero source credit to native engine bodies, upstream callers and this additional behavioral evidence. No area, story, quest, capture, encounter availability or renewability label is assigned to the raw byte, imported value or transition.

## Frozen producer identities

| Artifact | SHA-256 |
| --- | --- |
| `evidence/encounter/numeric_transition_producer_20261029.py` | `847d35514118ac13b581cfe38e4662351f2c82d4f6336d2821df562644cf8890` |
| `evidence/encounter/numeric-transition-producer-20261029.json` | `5129f8e8c42360bbf49faaf0e7f5f22b1b33dcbac396d1d0589c3aed3777b18b` |

## Standalone numeric accessor

`validate_scr_numeric_transition_20261029_batch04.validate(root, report_path=None)` returns one unit keyed by `(codeSha256,64612)`. Its SHA-256 is `ea6f463ee6792297ad091b561ae10eb19bdcb14d6165e8b221c9740570ed4020`. It explicitly depends on the frozen empty validator helper `c3e38cbf73c38d98484f799ba20e2fe05c34612dff4310949837eab6ebb94604`; no historical source or report is changed.

The accessor validates the frozen source/tool/fixture closure, current original-ROM and executable bytes, original archive aliases, generated body/report/image products and exact named allocation profile. It freshly re-emits the C source in an isolated source-only directory and compares current direct/private bounds, all three known slot read/write histories and named native API bindings. It independently reconstructs all128 scenario inputs and seeded persistent-state expectations, verifies every branch/thread/reentry/NaN case and bounded actual-return record, and validates the supported negative-entry path. It checks captured native proof rather than rerunning Unicorn; the original matcher remains the full native replay entry point.

An imported-module invocation from a different working directory passes. Local mutation controls reject a false actual-return record, removed NaN case and wrong scratch-slot identity. Missing or changed source-only products raise before any unit is returned. Integration should cache validated records only within one current measurement, then revalidate current inputs/products in each later measurement. These additional gates do not convert the still-unproved natural scene path into validated behavior.
