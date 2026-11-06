# ov000 raw-word setter caller alternative766, 2026-11-01

Existing ARM9 ov000 ARM0x02204DEC/292 receives a separate exact source alternative. It changes one declaration from void native_fn_0206e634() to u32 native_fn_0206e634(u32),retaining constant2 and discarding its result. All other source text remains identical to the old selected01da6dc55929 source. Fresh compilation and genuine MWLD reproduce all292 bytes,including288 instruction bytes and4 literal bytes. This adds zero functions and zero source bytes. Old source and shared preferences remain untouched.

Reproduce from any working directory:

    python C:/Users/trevo/Documents/RecProgramming/DQM/j2p-recovery-lanes/overlays/match_ov000_wordcaller766_20261101.py

ROM SHA-256674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6 and ov000 SHA-256783cb72f0d6ee2fdb632aba3e0ae41a9eee0c7e41933192b1680152e50aa61f6 qualify the identity. The caller invokes main ARM0x0206E634 directly,not0x0206E644. Actual setter instructions write low8 to0x021C4FC1 and preserve rawR0=2 before the caller proceeds. Its old signed-char source and the separately returning wrapper are migrated only through the coordinated save/core alternatives.

There are1,024 original/C pairs with2,048 actual top returns,512 actual setter returns and4,096 separately counted supplied service calls. Gate byte0x02238196 values0/1/128/255 cross every unsigned byte at0x02238197. Previous setter byte values permute all256 values on the active gate-zero path. Nonzero gate paths return that unsigned gate word without initialization calls. Active paths write setter byte2 and caller gate byte1; the final own raw return is0x02238190. These are raw observed words and bytes,not game-field meaning or legal live-state claims.

Each pair checks all core registers,CPSR,complete RAM including stack,raw call words and ordered writes. The four7-word0x02061C1C calls,two5-word0x0206E2FC calls,one1-word0x0206E6C0 call and one2-word0x0206E388 call use explicit zero-RAM supplied boundaries with legal caller-saved register/flag clobbers. Their real UI/resource behavior and complete formal types remain unproved. Two genuinely compiled/private-linked wrong sources return and fail the independent model: setter constant3 and writing caller gate byte2.

The save/core packet is frozen at commit0026b53da737e41ca91a70eb78ad4eef3cfa2ad8,manifest evidence/lanes/save-core/page-count284-ready-20261101.json SHA66f08d9508205793d8d49e2a61e7c4368bfa320193220d0c2de6d2845ac94712. Both main alternatives use u32(u32). Their sources,manifest and report hashes were independently checked in the peer lane and retained in the coordination JSON. They are provenance for joint integrator adoption,not hidden runtime dependencies of this caller reproduction. The caller fixture qualifies constant2 only; the peer proof owns the wider word-return domain.

No application,actual UI,host/device,scene lifecycle or save-persistence behavior is asserted. All initialization is synthetic. The integrator owns coordinated main/caller selection and complete module/ROM/regression acceptance. All earlier frozen source/proofs remain unchanged.
