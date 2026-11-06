# Field metadata C recovery, 2026-10-29

Eight main ARM routines compile and genuinely link to all 680 measured bytes as ordinary C. They are candidates for the integrator's next combined build; no shared registry or ledger was edited. The preceding 696-byte actor proof, positive SYS10 metadata-context proof, and all earlier sources and reports remain unchanged.

| Main ARM entry | Bytes | Measured behavior | Fresh unit profile |
| --- | --- | --- | --- |
| `020C55DC` | 156 | Load field-file pointer and initialize the original first 1,399 compact records | O2 |
| `020C5678` | 60 | Release file and clear manager when a handle exists; return zero when absent | O2 |
| `020C56B4` | 68 | Select loaded record access or existing cache fallback | O2 |
| `020C5714` | 60 | Scan all 24 signed cache tags for equality | O3, speed |
| `020C5750` | 108 | Insert a nonnegative absent key into the first nonpositive tag slot | O3, speed |
| `020C57BC` | 172 | Sort tags descending and refresh positive-tag payloads | O3, speed |
| `020C58C0` | 28 | Extract compact low twelve bits | O2 |
| `020C58DC` | 28 | Extract compact high four bits | O2 |

Each unit uses the pinned repository-local MWCC 2.0 SP1p5, ARM946E, inline off, and the real MWLD. Source is in `src/encounter/20261029-field-metadata/`; byte-identical hypotheses remain in `nonmatching/encounter/20261029_metadata16/`. All nine files contain 5 to 26 physical lines, without code comments or assembly. The true packed-u16 bitfields reproduce both extraction instruction sequences. Natural declaration ordering and pointer iteration recover the original register allocation; no register annotations or instruction patches are used.

## Reproduction and provenance

```text
python C:\Users\trevo\Documents\RecProgramming\DQM\dqmj2pro-decomp\nonmatching\encounter\verify_20261029_field_metadata.py
```

The final fresh replay passed from the parent DQM directory and produced the same report hash as the repository-CWD replay. The report retains exact source, object, native-range, compiler, linker and dependency hashes and all real link proofs.

| Artifact | SHA-256 |
| --- | --- |
| `nonmatching/encounter/verify_20261029_field_metadata.py` | `9a9809dac8f1564fcc713ffe00ac939da34ef2d29e7a3699978c4c3eefff05ea` |
| `nonmatching/encounter/metadata_fixtures_20261029.py` | `7d3598e0a4f8ecf6b46eb1bb920c2b98ab6b9503c1c4a7394f3643869dad00fb` |
| `evidence/matches/encounter-20261029-field-metadata.json` | `6a5c859e38bb1e45d1359ff170c23ea7890e2a52c9b365bbd45a025d24a45763` |
| `src/encounter/20261029-field-metadata/field_metadata.h` | `30d5f796e2505ea197325dd68455a4b5bac681ec224dcb86b2cdf7363b9cc9e6` |

Every source entry declares and precompilation-checks that header hash. Canonical boundary and current registry checks excluded ten previously accepted neighbors, including cache search `020C5868` and the separate kind-record getter `020449D4`. Fresh compiled source receives only its own candidate credit; original resource/allocator/VM/actor routines and already recovered callees receive zero new credit.

## Actual execution evidence

The original-versus-linked-C suite passes **399 actual returning outer calls per implementation, 798 total**, with 227 separately initialized machines per implementation. It compares R0 through R12, SP, LR, PC and CPSR; ordered CPU store addresses, sizes and values; persistent and VM data; the complete actor pool; field manager/cache and original mapped field image; kind manager/image; and the compact lookup. Each counted call must reach its return sentinel and preserve SP and R4 through R11. Native functions are not stubbed.

Cases cover 48 signed-key membership/insertion configurations, four independently modeled cache sorts and payload refreshes, loaded record access and unloaded cached records, 128 packed-word vectors through both extractors, zero-handle release, and 28 connected SYS10 returns using the two ROM-backed metadata tables. Cache-key vectors include negative sentinels, zero, duplicates, full caches, early empty slots with a later matching key, and values through signed16 maximum 32767. These are tag-operation tests and do not imply every key denotes a valid field record. Packed words cover all sixteen high nibbles and selected low values through 4095; extraction does not establish valid kind records.

Sorting changes tag positions before copying payloads for positive keys. Zero and negative keys keep the payload bytes already at their physical slots; the fixture checks this independently. The largest observed sort executes 110,125 native instructions. Sorting alone has an explicit 500,000-instruction cap and two-second timeout; constructors and SYS dispatchers retain the 100,000 cap, and other calls retain 20,000 with a one-second timeout. No counted call terminates by exhausting a bound.

All seven nonloader routines have actual-return coverage. During returning outer calls, the tracked source entries are reached 2 times for release, 349 for record access, 7,956 for membership, 393 for insertion, 4 for sorting, 156 for the low extractor and 128 for the high extractor, per implementation. These are executions, not unique recovered functions.

## Preserved unsupported behavior

The loader's entire 156-byte ordinary C body passes the compiler/linker byte gate, including its original hardcoded 1,399 bound. Its true native entry reaches a resource-context failure at main ARM `0200B534` after 146 instructions in the available synthetic context. It has **zero actual returning unit calls**. Positive file loading, allocator behavior and releasing a real nonzero file handle remain functionally unsupported. The 1,421-record modified file does not cause the original initialization bound to be increased.

An initial fixture incorrectly assumed that a missing unloaded-cache key would return null. Independent native execution contradicted that assumption. With the record base null and all 24 tags descending from 24 through 1, key 0 returns `021D5890`, which is outside the 24 cache payloads and inside adjacent compact-lookup memory. That returning pointer is explicitly marked invalid as a cache payload. Keys 25, 42 and 1420 instead fault at main ARM `020C588C`, inside the already accepted search routine. Its unsigned upper bound starts at 24 and can underflow when searching above the largest cached key. The controlled initial-assumption observations remain under `work/encounter-recovery/20261029/cache-fallback-initial-assumption-failure.json`; the final versioned report records all corresponding results and boundaries.

The three cache-miss faults and one loader fault are separate from the 399 actual returns. Their post-fault state supplies no proof. Matching C deliberately preserves these measured native paths. No added bounds checks disguise a behavioral mismatch.

The connected SYS10 cases use explicitly manual manager and compact-lookup initialization with the original field and kind file bytes. They do not execute native file loaders. Whole scenes, rendering, collision, malformed file headers/lengths, invalid record dereferences, script reachability, story/quest access and encounter renewability remain unproved. Packed bitfield layout and measured 32-bit pointer structures require a separate Android portability treatment. Whole-module acceptance and whole-ROM source reconstruction remain independent integrator gates.
