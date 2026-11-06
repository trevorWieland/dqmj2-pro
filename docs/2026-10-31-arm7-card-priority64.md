# ARM7 CARD priority setter: complete 64-byte ordinary C

Host ARM7 WRAM ARM entry `038026E0` is reconstructed as ordinary C across its complete 64-byte canonical extent: 60 instruction bytes and four generated literal bytes. The fresh source compiles and genuinely links to every original byte. It remains pending integrator module/ROM adoption, with zero original-data, helper-source, assembly or blob credit.

The caller takes a full unsigned priority word, disables interrupts, saves the previous common-state priority at `038090C0+F0`, stores the new word, invokes actual native `037FC3C0` with the original thread pointer `03809108` and that word, restores the captured interrupt state, and returns the previous full word. The C explicitly keeps a local common-state pointer across the calls; this natural lifetime gives the original register roles and one literal instead of the earlier 68-byte two-literal draft. No register forcing, assembly, object patching or fabricated alignment is used.

The compiler closure is the C source and two headers under `src/arm7/lane_20261031_card_priority64/`. The shared `native_card_types.h` bytes are unchanged from the reviewed previous CARD storage view. The common and argument storage views are 256 and 92 bytes; these are not claims about complete original allocation sizes. `CardThread` is passed as an opaque address to the existing native scheduling API, with no newly claimed scheduler source coverage.

Reproduce with Python 3.13.5:

```
python C:/Users/trevo/Documents/RecProgramming/DQM/j2p-recovery-lanes/arm7/match_arm7_lane_card_priority_20261031.py
python C:/Users/trevo/Documents/RecProgramming/DQM/j2p-recovery-lanes/arm7/validate_arm7_lane_card_priority_20261031.py
python C:/Users/trevo/Documents/RecProgramming/DQM/j2p-recovery-lanes/arm7/audit_arm7_card_priority_transport_20261031.py
```

The positive suite executes original kernel initialization, scheduler disable and original CARD initialization before the owned entry. All original IRQ, SetThreadPriority, list insertion and rescheduling helpers remain real native code with no lower providers. Scheduling stays disabled, and any context save/load is a failure. Thirty raw priority/previous-word cases across four entry flag states produce 240 actual original/compiled entry returns and 1,632 separately observed native helper returns. Each side uses a fresh machine and compares complete register/CPSR/stack/mapped-memory/read/ordered-write evidence.

An independent own-effect model checks the previous full-word return, the F0 store, actual helper argument words and actual thread-priority word at `thread+54`. Complete helper-memory effects are compared, without claiming an independent full helper model. The real initialized common and thread priority is four. Previous common words zero and FFFFFFFF are explicitly synthetic overrides; new priorities above31 are raw synthetic inputs, without an ordinary-validity, concurrency or enclosing-game reachability claim.

The initial model mistakenly sampled `thread+58`, the profiler field, as the priority field. Its failure is preserved separately; the complete native loads and reviewed thread declaration place priority at +54. Two pre-publication harness failures (stale promoted source-root spelling and inappropriate reuse of the callback-supplement boundary helper) are also retained. The corrected source-only guards use the existing canonical entry without expanding its namespace or initialized denominator.

The standalone validator performs a fresh source/link/native replay, verifies current products before its cache, and pins the original execution inventory. All 31 controls pass. Three same-size wrong C bodies change the previous word, stored word or thread pointer; each genuinely links, explicitly returns in a fresh native machine, and then fails the independent model. Missing/corrupt current products and false source/ABI/coverage/return claims are rejected. The bounded one-instruction run remains unsupported with zero return credit.

No BIOS, physical scheduling, emulator, live input save, application adapter or Android device is used. The TI925T Unicorn execution model is a surrogate for these bounded ARM7 contexts. Current hashes, alternate-working-directory replay outcomes and source-only transport closure are recorded in the companion receipt and handoff manifest.
