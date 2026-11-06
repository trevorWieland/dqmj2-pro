# Item word input and full absent sentinel - 2026-10-31

ARM02066A7C/32 is a new ordinary-C candidate. Replay `python match_mechanics_save_20261031_lane_item_byte.py`. Normal and parent-directory Python `-I -S` runs reproduce canonical SHAbfb789e5d9323fcae3fad71bc5eba4211e7689cab949573953b4384f5ca8e5ad. Recorded compiler path/hash/complete flags are static inputs. Full compiler/MWLD/native bytes match with current object/link provenance checked independently. No registry/module/ROM mutations are performed here.

The preferred C explicitly forwards full incoming R0 into actual02065D88 and uses an explicit pointer conversion of its raw return. The native getter loads the base at021C2AB4 and computes base+88*item with ARM32 modular arithmetic. The caller reads descriptor+2C:only raw8 selects the byte at+2A;all other selectors return full FFFFFFFF. Selected byteFF returns255,which is distinct from absentFFFFFFFF. The old u8 result temporary collapsed that distinction,and its omitted argument was an incomplete C call contract despite incidental physical R0 retention.

The actual measured ItemTbl file is22,536 bytes:8-byte header plus256 records of88 bytes. SHA is5aa45bb4c0de39185246defd9698ae28edef64144d30c583751b16beb5eb64b7. Every actual record,including index255,is tested. This uses the original extracted asset bytes rather than scenario-only field guesses. Descriptor offsets and literal8 are measured;no skill/book/category interpretation is assigned.

The1,316 supported pairs yield2,632 actual top returns and separately2,632 actual native getter returns,with zero providers or data writes. There are256 actual-asset and1,060 synthetic contexts. Synthetic tests cover all selector/result bytes,multiple ordinary indices,and sparse high-word/native-wrap aliases. Those sparse backing experiments do not establish valid game item IDs,original allocation extent,portable callee array bounds or import limits.

Every invocation uses fresh Unicorn state,requires native call edge/input/return,SP/callee-saved restoration,exact ordered reads,unchanged table/descriptor bytes and all eight own instructions. Actual backing256,before-table and null-base original/source profiles give six excluded stops without handled-error or post-fault claims. The original file is unchanged.

Two full compiled wrong-C controls truncate the absent result or change selector8 to7. Their2,632 pairs yield5,264 actual returns,1,419 independent rejections and1,213 positives. No false binary execution difference is claimed for an old omitted-argument source where identical bytes happened to retain R0. Full evidence is deterministic gzip.

Original ROM/save,application and accepted source remain untouched. No ordinary scene,lifetime,semantic save offset,bank arbitration or chronology inference follows from this routine. Integrator source/module/ROM gates remain required.
