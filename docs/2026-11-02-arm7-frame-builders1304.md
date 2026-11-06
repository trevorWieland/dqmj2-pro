# Seven host ARM7 frame builders

Seven complete ordinary C functions genuinely compile and link to 1,304 native initialized bytes: 1,248 instruction bytes and 56 generated literal bytes. Run `python validate_arm7_sdk275_frame_builders_20261101.py`. The new source, exact profiles, per-caller runtime-word policy and native model are frozen independently of shared registry/configuration updates. Whole-module and ROM acceptance remain integrator-owned.

| Host main ARM entry | Ordinary C | Bytes | Paired cases |
| --- | --- | ---: | ---: |
| 027F16B0 | MakeDisAssFrame | 124 | 8 |
| 027F172C | MakeAssReqFrame | 168 | 64 |
| 027F17D4 | MakeReAssReqFrame | 180 | 64 |
| 027F19FC | MakeReAssResFrame | 352 | 768 |
| 027F1B5C | MakeProbeReqFrame | 140 | 64 |
| 027F1E08 | MakeAuthFrame | 192 | 1,092 |
| 027F1EC8 | MakeDeAuthFrame | 148 | 1,080 |

The normalized accepted131 export independently contains none of these seven qualified identities. The 124-byte routine was already exact in the earlier diagnostic campaign, while the other six gained genuine linkage after helper source-visibility changes; this distinction does not make 124 bytes previously accepted source. Final duplicate selection remains the integrator's responsibility.

## Execution and source-only rebuilding

The fresh original/compiled-C suite has 3,140 pairs and 6,280 actual owned returns. It separately observes 39,420 nested helper returns, 57,016 actual setup returns, and 6,280 actual clear returns at the descriptor-prefix boundary. The enclosing prefix receives zero constructor-return or source credit. All 312 owned instructions execute within the deterministic supported corpus. No provider results are substituted.

The fixture retains real queue, mode, CAM, TX, OS heap initialization/creation/current-heap selection, allocation, header initialization, byte accessors and related lower routines. Original and compiled executions compare raw registers, flags, stack, full mapped-memory hashes and ordered writes. Independent checks cover allocation arguments/capacity, owned store order, return pointers, status/control/length fields, rate/SSID payloads, copied MAC fields, fatal-bit effects and management selection. Actual helper source is an uncredited dependency rather than reconstructed by this packet.

Nine separately compiled wrong C variants produce 5,312 actual returns and 2,332 independent-model rejections. The validator passes 302 controls: 80 metadata/product, 158 direct policy, 56 native prerequisite and eight source-domain controls. Missing/changed compiler products and native traces withhold validation. Default unknown-data/function policies remain unchanged, and the narrow word binding restores the base handler after success/error.

The cold receipt `evidence/verification/arm7-sdk276-frame-builders1304-cold-20261101.json` preserves the old output directory, starts with no dedicated WORK path, and invokes the full suite from an unrelated CWD. It reproduces identical positive/control hashes without copying caches. An unfrozen Python helper's CRLF/extra EOF blank line was normalized before freeze, followed by complete warm and cold replays; C, compiler flags and native bytes stayed unchanged. The earlier control-selector error and formatting receipt remain explicit failed-development evidence.

## Concrete native boundaries

Compiler layout measures WlCmdHeader as four bytes, HEAPBUF_HEADER as twelve, AUTH_FRAME as 306 and CHALLENGE_ELEMENT as 255. The actual auth allocation argument is therefore `61 + word`; it is independently checked at the real AllocateHeapBuf call. With the original 2,048-byte native heap and 32-byte cell/rounding behavior, word1943 succeeds and word1944 fails. Twelve larger-arena cases genuinely allocate for 65533/65534/65535 and exercise u16 body-length wraps5/6/7 and byte challenge-length narrowing. No success return is injected.

For response AID exhaustion, the fixture initializes a 16-record CAM context and calls original CAM_AllocateAID on records1..15, checking each actual successive return. The subsequent real owner call reaches AID0/status19. Nonzero supplied status bypasses owner AID allocation. These are bounded native state effects; no protocol legality, normal-game access, client ownership or real caller reachability is assigned.

The management helper compares two zero-extended u16 fields with a signed expression `count < 24 - connected`; native uses the signed LT/GE conditions. Synthetic count/connected edges, full nonzero check words, allocation failure, null/provided SSID trailers, rate bit patterns and raw u16 reason/status/challenge words are exercised. Synthetic fields are identified explicitly rather than presented as ordinary reachable population states. Invalid MAC/CAM storage, changed modules and instruction exhaustion have no post-fault or normal-return credit. Declared u16 overflow and SSID array-capacity refusals are separately scoped source-input controls.

## Types, provenance and limitations

The comment-free C and closed type hierarchy derive from comparative ntrtwl/NitroSDK revision ccbbcc8b6db4c4dbba3d503d2026978d78977840. The historical game SDK revision is unproved, and no CC0 or original-assembly attribution is inferred. Only static function declaration/definition visibility was changed to make actual helpers independently linkable; static data stayed untouched. Objects, opcodes, relocation addends and registers are never forced or patched. All compiler inputs are five repository-local C/include files without parse shims, system headers or assembly definitions.

The reconstructed WL_MAN view is 0x694 bytes and is backed by the measured descriptor clearing span; this does not assert the total original allocation extent. Pinned MW long/pointers are four bytes. The SDK uses variable-length packet layouts and reserved/rounded allocation storage. This packet establishes matching code and tested physical ABI/effects under that target; ISO-C object/provenance details and Android LP64 portability of those packet views are explicitly unproved. Native hardware, interrupt/concurrency behavior, full protocol input space and enclosing scenes remain outside this bounded proof.

Only the seven owned functions receive candidate credit. Additional C definitions, original rate data at027F74D0, lower helpers, setup functions, descriptor prefix and any unchanged scaffolding receive zero new source/data/denominator credit. In particular, the unqualified InitTxCtrl callback at027F0950 and local-data refusals remain intact in separate research.
