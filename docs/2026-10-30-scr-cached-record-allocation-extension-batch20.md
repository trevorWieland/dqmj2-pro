# Original free-pool allocation under qualified cache contexts — 2026-10-30

This new companion proof broadens the measured native contexts for the two frozen
624-byte routines from [batch 19](2026-10-30-scr-primary-runtime-configuration-batch19.md).
It freshly recompiles their existing C/header/profile closure and compares original
versus rebuilt complete SCR execution. It adds zero source bytes, definitions,
native bytes, images, or whole-ROM match credit. All prior source, compilers,
fixtures, reports, and shared registries remain unchanged.

The original constructor overlay000:ARM02212C94 scans 16 records at `02243E3C`,
stride `10C`, for zero active byte `+105`. The new corpus supplies free rows 0,
15, or both 0 and 1, then enters the complete script twice without resetting the
pool. Actual results are 0 then -1, 15 then -1, or 0 then 1 respectively. The
returned native index is converted to binary32 in VM argument register 0. The
whole pool and all 14 ordered field writes are checked, including coordinates,
scale words, category byte `+106`, mode byte `+107`, selector halfword `+100`,
byte `+108`, and active byte `+105`.

Original resource helper overlay000:ARM021DF950 first searches 16 IDs at `02231F64`,
stride `30`, using original ARM021DF544. Category 6/7 resource IDs are measured
signed halfwords 119/190 in original overlay data at `0222BAF4`. Two synthetic cache
contexts place that matching ID in slot 0 or 15. The real helper returns 1 before
reading the deliberately null data pointer `02231BF8`. This proves the measured
ID-cache predicate, not valid resource bytes, graphics readiness, or natural scene
initialization. Random bytes outside those cache IDs remain unchanged.

A third context fills all cache ID words with unmatched nonzero values. Original
free-cache search ARM021DF578 returns -1; the resource helper returns 0. The
constructor still finishes writing/activating the selected pool record and returns
its index. Its caller does not gate that record allocation on the helper result.
This does not make the resource context valid and must not be presented as a
successful rendered object or a scene-level availability rule.

The corpus has 72 fresh contexts: both script routines, threads 0 and 3, three
free-row layouts, three cache layouts, and both primary-flag outcomes. The existing
scalar profiles rotate through fractional values, half ticks of both signs, signed
zero, and the qualified coordinate endpoints. Two serialized calls per context
and two implementations produce 288 complete own-entry executions, 6,984 actual
native returns, and 192 separately observed nested resource-helper returns. The
resource-helper return is observed at its real saved LR after native execution;
no PC, register return, instruction, function, or provider is substituted.

Both original functions, the dispatcher, float conversions, primary getter, entire
constructor, cache lookup, cache-slot scan, and resource helper execute unmodified.
The normal instruction/time caps remain 20,000 and 1,000,000 microseconds per native
call, with a 40-record SCR bound. This proof does not adopt count-only execution.

The comparison includes all general registers/CPSR, ordered native CPU stores,
whole VM state, all 256 VM slots, persistent bytes, full pool, full cache, argument
bank, eight constructor arguments, and actual nested return values. The independent
verifier derives initial entropy, first-free choice, all field writes, carry into
the second call, coordinate conversion, shared module stores, argument clobbers,
and complete traces. It performs fresh source-only rebuilds in isolated directories
before validating the current products. It rejects ten mutations, including a
false allocation index, wrong record byte, false return, lost nested return,
invented asset proof, duplicate source credit, and cross-root native provenance.
Root-directory and parent-directory runs pass with identical verification output.

A fresh free-pool, empty-cache, null-data-pointer control still faults at original
`021DF9A4` with an unmapped read. It is reproduced for both script images. Its
prefix return count is diagnostic only; complete-entry, source, and post-fault
state credit are zero. Unsupported paths are not repaired or treated as success.

Reproduce full native/source-linked context evidence:

```powershell
& 'C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe' 'C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\match_scr_cached_configuration_20261030_batch20.py'
```

Replay current source-only evidence and mutation controls:

```powershell
& 'C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe' 'C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\verify_scr_cached_configuration_20261030_batch20.py'
```

Frozen identities:

- Matcher `f56de7696bb9ae722aa929ae588587db20c567269eb508f3cdce47128ba08f52`.
- Evidence `evidence/encounter/scripts-cached-configuration-contexts-20261030.json`:
  `417232d9b05d16d260a447111ae3526967dd7fc07101f0fc214d562c23532a78`.
- Independent verifier `eb22c4b376561d962a3da2da10aedbef264fd7af38b8b1fc4e88ef0974217409`.
- Verification `evidence/verification/scr-cached-configuration-contexts-20261030.json`:
  `f436de9e6dd46779a68e2157b7524148aea6ed894826eedd6490214b3e58d1fd`.

The report pins all reused source/backend/helper files, current original ROM and
native modules, actual native root, exact emitted bodies, and current products.
It does not infer story labels, ownership, import legality, access, renewability,
asset readiness, or natural enclosing scene reachability.
