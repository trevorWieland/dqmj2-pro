# Explicit slot and third-word callers - 2026-10-31

Main ARM0205F210/108 and0205F6A0/108 are now genuine compiler/MWLD full-byte matches. The first explicitly forwards its bounded slot index to the already accepted0205F2D8(s32). The second requires a third fullword input,forwarded through original02038148 on a nonnull handle/type!=2 path to original020379C4. That routine saves incoming R2 and stores it at node+0C. This measured store explains why native preserved R2 while the intermediate two-input hypothesis reused it for the global array base. No register forcing,artificial padding or opcode patch is used.

The intermediate typed two-input draft,after restoring R1,remained106/108 and is retained as a known incomplete hypothesis with its own hash. It was never accepted. The preferred three-input source matches108/108 and observed state effects. Original raw m2c drafts and all accepted sources remain untouched.

Measured runtime rows begin at021B8B10,with16 entries of8 bytes:word+0 is a handle pointer,signed16+4 controls the initial branch,and byte+6 is written by the second caller. Unsigned indices>=16 yield raw0 and code-byte12;negative signed16 fields yield raw0/code8. The second caller additionally rejects unsigned input1>127 with raw0/code16. Otherwise both finish through the real0205ED58(code0),which stores the low code byte at021B8AE1 and returns raw1. These numerical branches are not assigned game-success,volume,frame or scene meanings.

For first-caller valid rows,the real0205F2D8 rechecks the same signed16 field and clears the code byte. Static isolated nonnegative rows therefore return1. The source still preserves the original conditional. Six paired profiles explicitly inject FFFF into the halfword at getter entry to exercise its0 branch;the actual getter executes afterward. There are12 injection events across native/source runs. This is a synthetic RAM perturbation,not evidence of actual concurrent mutation.

Real020380D4 tail-loads the handle and transfers via verified BXIP to02038554;they share one physical return. A nonnull handle with nonzero byte+2C selects either supplied38708(handle) when input1==0,or actual379C4 followed by supplied3887C(handle,0) and a byte+2C store2. The actual379C4/379EC state calculation reads four words at handle+1C/+20/+24/+28. Its current-value helper takes the signed direct-target path or a bounded supplied signed division. The update stores evaluated current,new target,full third word and zero progress. No original device/object-lifetime semantics follows from these synthetic handles.

For second-caller nonnull/type!=2 paths,38148 shifts the bounded input1 left8 and calls379C4 with the complete incoming third word. Values0/1/100/80000000/FFFFFFFF and the deliberate global-array-address alias are measured at the eventual word store. Null/type2 contexts preserve node state. This actual path qualifies input necessity;it does not prove ordinary scene prerequisites. The below40000 helper sources are read-only and receive zero source credit here.

The producer executes1218 native/source pairs,2436 actual top returns and4856 separate actual helper-return instructions. There are480 supplied lower calls across three kinds:nonzero-denominator26144 division,38708 and3887C. Original38148,380D4/38554,379C4/379EC and accepted5F2D8/5ED58 execute physically. Source runs patch both new callers and freshly rebuilt72 accepted helper bytes together,adding zero duplicate coverage. Existing5ED58 s8 source remains appropriate to these measured caller values0/8/12/16;no broader error API migration is asserted.

Four complete wrong-C bodies execute2610 paired cases/5220 actual top returns:wrong getter index,known missing third word,truncated third word and exclusive127 bound.506 output/store/backing/lower-contract differences independently reject;2104 are observational positives. Register/read/call scheduling alone is not a semantic rejection. Coincidental third-word-equals-array-address cases preserve an explicit control for the malformed two-input source.

All26 own instruction starts per caller,full argument frames,raw returns,ordered effects,complete backing/canaries,actual termination and SP/callee/control restoration are checked. Deterministic gzip sidecars preserve cases after per-range backing SHA compaction. No host sound,emulator,Windows/Android execution,bank selection,whole-game or module/ROM acceptance is claimed.

Reproduce from any working directory:

`python <repository>/match_mechanics_save_20261031_lane_status_cluster.py`

Normal and parent-directory -I -S replays reproduce canonical SHAd251ace8b55b8166e235b1f5a5e8fe715f6b2cfc2a2abaf894a4893405d6a893. Root owns source registration and full module/ROM validation. Net new candidate coverage is two functions/216 bytes only after those gates.
