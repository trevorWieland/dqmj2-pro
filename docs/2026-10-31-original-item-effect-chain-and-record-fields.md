# Original item effect chain and record fields - 2026-10-31

This zero-credit extension executes original C888,C6E0 and C7EC with the previously recovered32-byte selector. Replay `python prove_save_core_item_effect_chain_20261031.py`. Normal and parent-directory Python `-I -S` runs reproduce receiptf170b4f390b7d33c1bb32c942925cca21a4dd5bdd5a49863e2ab745c2486fcca,producer552313316e706073a91a7b1f10063696cfab4131c83fb0c64e972065988dbdc9 and native case digestabb91e368743e334ba14cf35371609ac69311c2de6d66e58a1aea72ce901a4c3. C888 already has accepted source in src/overlays/ov001_20261031_reroll59/reroll.c,SHA596e11dccf2051376ca26986cbbc6dbadc74b6c20fbddcc9988217e55628be1f. It is reused as existing coverage,never duplicate recovery.

The actual caller,C6E0/C7EC,DB8D0,DB438,DBCBC,DB788,main7C2B8/7C1E4/7B674/6259C,overlayD96D4 andmain42C0C execute. The two supplied boundaries are conditional ov001021DC4CC(actor,1,0) and022024D4(two byte coordinates,negative requested word). Neither boundary's real policy,effect or downstream changes are established. They preserve callee-saved registers,legally clobber caller registers/flags,make no memory writes and return declared raw words.

| Measured location | Local behavior |
|---|---|
| Item descriptor+30 | Exactly1 replaces the incoming target by actualDB438(index,0) and processes three440-byte records. Other bytes process one incoming target. |
| Actor+31C,+1FF | Both nonzero enter the supplied DC4CC policy;any nonzero raw policy result permits the following mutation. |
| Actor+31C,full pointer+1E8,pointed record+AC | Otherwise originalDB8D0 requires nonzero31C,zero1FF and record+AC0. Only then descriptor+29==1 permits mutation. No status or ownership names are inferred. |
| Actor+1EC and+21C | Signed16 inputs to the original ceiling calculation,under raw global020DDD40=0. |
| Pointed record+46 | Original7B674 counts requested byte IDs until0 or64 entries. Original7C1E4 combines IDs80..89 with measured weights5,10,15,20,22,24,26,28,30,35. Duplicate and early-zero effects are tested. |
| Actor+1F0 | OriginalDB788 writes the requested value clamped to the measured nonnegative ceiling. Only this signed-halfword view is claimed. |
| Actor+320 | C6E0 clears the halfword after the supplied lower effect on each permitted record. C7EC later reads it signed. |
| Actor+160,+10D | When old160<31,C7EC doubles signed320,caps only above31,masks to a byte,and originalD96D4/main42C0C write160 and10*byte/31 into10D. |

Within the explicitly nonnegative0..9999 ceiling domain,the original path computes floor(descriptor+2B*ceiling/100)+1. A request above the ceiling is clamped for the1F0 store,but the lower effect still receives the negative pre-clamp request. For ceiling0,request1 therefore stores0. Raw descriptor percentages0/1/50/100/255,ceilings0/1/100/9999 and counted-record variants are measured. No assertion about an original healing/stat type,quantity or paid operation is made.

C7EC initially returns1. If a processed160<31 and doubled signed320<=31,it sets return0;otherwise the return remains1. Negative signed320 is not floored before byte conversion. For example-1 requests byteFE,which the original writer stores as254;its scaled10D byte is81,while the current C7EC return is0. These are actual live-record effects;subsequent frame scheduling and320 producers remain unresolved.

The252 independent profiles yield504 actual caller returns,28,670 separately observed actual native dependency returns,820 supplied lower calls and568,554 executed instruction events excluding provider entries and stop hooks. All66 C6E0 and39 C7EC instruction starts are observed. The stat path remains limited to raw feature020DDD40=0;four instructions in7C2B8's alternate branch are outside this oracle. The caller has84 instruction starts here;the separate frozen1,907-case oracle covers its88 starts. No instruction count is source credit.

Exact ordered actor changes and caller/RNG writes,full440-byte canaries,unchanged178-byte disposable records/assets,native call/return contracts,SP/callee-saved restoration and actual bounded return are checked independently. Two actual ItemTbl records9/243 are used;synthetic percent/selector29/multi fields,records,progress and flags are explicitly supplied. Every pair uses isolated machine state. Original input files remain hash-unchanged. No new serialization offset,bank arbitration,chronology or meaning for the40,560 unknown save bytes is claimed.

Four invalid-target/null-record original/source runs stop without return and receive no post-fault claim. The initial new instruction manifest underestimated7C1E4 and overextendedDB788;the guard rejected execution before return credit,and measured extents212/68 were applied before final replay. The failed attempt is retained separately. No frozen source,previous proof or original bytes were changed.

This establishes conditional record mutations and local data flow,not ordinary scene reachability or inventory consumption. In particular the actual DC4CC and22024D4 behavior,record lifecycle,020DDD40-on branch,saved-state persistence and links to allocation02076D70,slot02062F3C,rebuild02078978 orlibrary0207AEBC remain unresolved. All evidence is deterministic gzip and all source/module/ROM credit stays with the integrator.
