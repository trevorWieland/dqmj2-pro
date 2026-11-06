# Heap construction and request words — 2026-11-01

The queued package contains seven new ordinary C functions covering 1,152 initialized native bytes. Acceptance requires its own complete build and committed closure. Byte coverage is distinct from overall game completion, and original-object scaffolding remains in the ROM build.

The identity is the authoritative ROM SHA-256 `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`, ARM9 main module, mode and address. Reports retain target/source/object hashes, compiler profiles, input dependencies and reproduction commands.

## List count and heap initialization

`python match_main_list_count60_20261101.py` qualifies ARM 02009A98/60. Its 960 original/C pairs produce 1,920 actual top returns and 3,840 actual original IRQ-helper returns, with no supplied outcomes. Independent shuffled lists contain zero to 128 nodes; full RAM/global effects, count, control masks, callee-saved registers and stack guards are checked. Both cyclic bounded execution and one-instruction exhaustion receive zero completed-return credit. Two wrong C bodies physically return 276 times with 260 model rejections and 16 unchanged cases. Alternate-directory isolated-Python replay passes.

`python match_main_heap_initializers276_20261101.py` qualifies ARM 0202B914/160 and 0202AE28/116. There are 2,400 original/C pairs plus 1,200 executions composed from both recovered C bodies, totaling 6,000 actual top returns. The 60,150 lower completions comprise 58,950 original-helper returns and 1,200 source-linked header returns; these are subsets of one total, not additive alternative totals. No helper outcomes are supplied.

Independent models cover low-byte option storage, the measured debug-fill word, child/root list initialization, empty and nonempty insertion, nonfirst/nested parent selection, sibling links/counts and expanded-heap free-block fields. The initialization flag is a complete word: nonzero values with a zero low byte must remain initialized. The option getter returns a 16-bit value, and the span calculation occurs before conditional fill. These source lifetimes and types recover the native code without instruction patches. The header routine is declared void; its raw R0 is compared without inventing a public return contract. Four wrong C bodies return 372 times with 258 independent rejections.

The comparative heapcommon.c is pinned to the same public commit as the earlier heap reference, with its Git blob independently checked. It is an unmodified copied reference input, not compiler input or new source credit. The comparative revision's no-use fill macro is empty; the measured game's conditional fill behavior is retained. Equal historical SDK revision, debug policy, threshold and formal-type provenance are not asserted.

## Heap search pair

`python validate_main_sdk_heap_search356_20261101.py` qualifies ARM 0202B044/180 and 0202B0F8/176. The typed block/expanded-heap views and explicit alignment temporary lifetimes inside the nonempty-list guard produce exact complete links under their demonstrated compiler profile.

The 560 cases per function produce 2,240 original/compiled own returns. Original commit completions and freshly source-linked 424-byte commit completions are separate groups of 612 each; 8,308 other original lower-helper returns are tracked separately. Multi-block independent models select nonfirst nodes in 69 forward and 82 backward cases. Thirty-four metadata/availability controls and four genuinely compiled wrong-C controls pass; the latter return 2,240 times with 843 independent rejections. Helper/data extent and denominator credit stay zero.

Its reference-only input consumer is added only after the previous package's committed source closure exists. The updater verifies the proposed exact producer hash, ARM9/main/mode/addresses, source-only compiler inputs and prepared registry membership. It preserves every existing ledger entry. Default ARM7 namespace/data refusals remain unchanged. The input auditor requires the resulting consumer ledger to equal its committed Git blob.

## MMIO and request caller

`python match_mechanics_save_20261101_lane_mmio_initializer.py` qualifies ARM 020431D4/304. The native display-control accesses are full words; the recovered views are explicitly volatile. The corpus has 32 parent returns, 96 original fill returns, 320 explicit lower calls and 6,299,648 losslessly RLE-recorded stores into private simulated MMIO/VRAM. Four wrong C bodies return 16 times with 14 independent rejections and two unchanged cases. Bus-width and cross-region ordering controls reject even when final bytes agree. This establishes simulated payload/order behavior, not physical hardware or Android-device behavior.

`python match_mechanics_save_20261101_lane_request_mask.py` qualifies ARM 020BAAF0/156. Caching the unsigned lower result before comparing it resolves the final two bytes. The 806 pairs produce 1,612 parent returns, 31,866 original-helper returns and 14,030 calls to one explicitly supplied boundary. The original Thumb callback setter, mask loop, current-byte getter and four-word thunk execute. The callback holder at 021D2308 and getter holder at 021D19E0 are distinct. The rejected shared-holder model failed before execution and receives zero credit. Four wrong C bodies return 32 times with 15 model rejections and 17 unchanged cases. Network, persistence, ordinary-scene and callback-execution meanings remain unproved.

## Preserved research

The ov003 configuration draft remains inexact: 772 linked bytes versus 756 native, with 545 equal bytes. Its bounded models pass 160 pairs/320 top returns, 1,408 original dependencies and 736 supplied calls. Twelve store-order differences and twelve extra raw argument views remain explicit. All 744 native instruction bytes are observed; 12 literal bytes are classified separately. The initial wrong byte-table model remains a separately replayable rejected experiment. This packet adds zero accepted coverage.

Three further typed heap/list helper hypotheses currently link exactly at 44, 44 and 84 bytes. Their standalone/source-composition qualification is still pending and they are excluded from this package's accepted function and byte totals. Cyclic/corrupted/concurrent heaps, arbitrary aliasing, complete source-only ROM reconstruction and the full Windows game remain unproved.
