# Explicit forwarded destination,holder and index - 2026-10-31

The accepted main ARM0204106C/12 is a literal-load/BXIP tail thunk. Its historical C declares void and calls02028B64 without explicit arguments. Original224-byte28B64 saves incoming R0 destination,R1 holder and R2 unsigned index before any lower call. It calls original76-byte8C58 to clear256 destination bytes,then dereferences the holder and executes original16-byte2BEDC header lookup. Thus this is a path-qualified consumed-input contract,not a conclusion from incidental register reads. Original C and native bytes stay unchanged.

The separate preferred ordinary-C alternative explicitly forwards(void *destination,const void *holder,u32 index). Pinned Metrowerks compilation and genuine MWLD reproduce all12 bytes. It adds zero functions/bytes. A qualified actual BXIP opcode,IP target and unchanged LR prove tail transfer;the original224-byte body shares the top return and is never counted as a second host invocation.

The native/source fixture has384 pairs/768 actual top returns,1536 separate actual8C58/2BEDC return instructions,and768 observed dependent tail entries. Two explicitly supplied lower boundaries,2E958 and2F520,occur336 times across paired runs. The first copies16 synthetic selected-node bytes;both clobber legal caller registers/flags. Their original resource/geometry semantics remain unproved. All own thunk instructions are covered;complete backing/canaries,ordered reads/writes,full call frames,raw return,actual termination and SP/callee/control restore are compared.

Deterministic packed headers support counts0/1/2/255 and full indices0/1/2/254/255/256/80000000/FFFFFFFF,two holder addresses,three aligned destinations and two independent register seeds. Valid selected nodes produce native raw1 and initialization stores;out-of-range indices produce raw0 after the real clear. These values are not assigned a game-success meaning. Six null destination/null holder/holder-erased-by-clear runs stop at physical bounds,with no return or post-fault credit.

Two complete wrong-C bodies force index0 or shift destination4. Their768 paired cases/1536 actual top returns produce720 independent output/backing/call-contract rejections and48 observational positives. Original dependency bodies remain real. Historical source is not treated as a failing ARM binary;the existing native thunk retains registers and is byte-identical.

A hidden Windows PE32 process compiles and executes the preferred C384 times. Its separately modeled three-argument lower body consumes each pointer/index and matches the complete6144-byte native destination/canary golden backing plus raw result. Another384 native captures repeat the same frozen profiles for port input;they are not extra coverage. The old void/empty-call source fails compilation against the explicit API. No old Windows binary failure is fabricated,and this is not a port of the original224-byte dependency,an Android run,a64-bit result or a whole-game proof.

Reproduce from any working directory:

`python <repository>/match_mechanics_save_20261031_lane_forward_animation_abi.py`

Normal and parent-directory -I -S replays reproduce canonical SHA26e24551e8349c30282a02802853cb084419e2a4bbf768af3e67a6632a1e86d6. Current object hashes are compared with current real-link validation,while native/source/profile identities and case digests are fixed. Source/machine/controls/gzip/native dependency identities and pinned Windows tools are explicit. Root alone owns preference migration and whole-module/ROM acceptance.
