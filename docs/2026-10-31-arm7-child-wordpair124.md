# Child ARM7 complete quotient/remainder caller

The complete `dwc/utility.bin/move/child.srl`, `utility-child-arm7-main:ARM027F6A48/124` routine now genuinely compiles and links to every native byte. Its 31 ARM instructions have no literal pool or padding credit. The measured profile is MWCC 1.2/sp2p3, O2/space, ARM7TDMI, with the declared flags and unchanged object relocations passed to the independently pinned MWLD. No assembly, original executable object or dependent routine receives source credit.

The original generated draft used an undefined `SECOND_REG` pseudo-helper to obtain R1 from a native divide. Its object could compile but its interface did not reconstruct the actual behavior. Ordinary C now declares a separately named, address-qualified `u64` ABI view. The low 32 bits describe the original quotient in R0; the high 32 bits describe its remainder in R1. First uses explicitly select the low word, and the final call selects the high word. This is a measured pair of 32-bit ABI results, not a claim that the original operation divides 64-bit operands.

An accepted older consumer at `src/utility/translated08/native_utility_child_arm7_main_027e3a18.c` already declares the original helper name with a `u32` return. An initial unaccepted candidate reused that name with `u64` and achieved identical instruction bytes, but its C declaration closure conflicted. That candidate remains historical. The final caller uses `native_utility_child_arm7_divpair_arm_03805184`; the old consumer and its declaration remain byte-identical. The unchanged linker independently binds each actual BL relocation to the same original ARM entry. A genuinely compiled conflicting-name control still links exactly before the declaration gate rejects it.

All three input words and the source arithmetic are unsigned 32-bit values. Adjustments, the multiply and additions wrap before the final remainder, including synthetic zero and high-bit arguments. The independent integer model covers the native adjustment for second words 1 and 2, four actual nonzero divide calls, and the final R0. No calendar, valid-date, story, access or game meaning is assigned to this arithmetic pattern.

The complete original/rebuilt fixture has 448 vectors and 896 actual own-entry returns. It observes 3,584 separate actual returns through the original divide entry, retaining the complete R0/R1 result and callee-saved state for each call. Fresh Unicorn 2.1.4 TI925T ARMv4T-surrogate machines execute all original callee instructions. No provider replaces arithmetic. Raw registers, APSR, stack effects, actual return PC and the independent wrapped-word model agree. Every own instruction address is visited. Budget stops remain unsupported with zero return credit.

The 40 caller controls pass, including source/runtime closure, mode and program identities, current missing products after cache population, raw register-result errors, compiler-built wrong arithmetic/return/prototype variants and rejection of generated pseudo-register helpers. Its standalone validator first regenerates the pinned source report, preserving clean invocation without an old object cache. Root and unrelated-CWD replays produce identical report and control bytes.

Canonical match report SHA-256 is `5ba35c4897ec05f61a4eb80c77d5e8c60a6558b8fe03f33b83223c574b493698`; the 40-control report is `a333e0c0c2b59452ec4f04610c334a3a2dbcc6677e59b2d52656b91115ab2c97`.

## Original divide code-scope gap

The original entry `utility-child-arm7-wram:ARM03805184` is configured as only eight bytes. Its natural computed/unrolled execution extends through the return at `03805364`; the decoded span is `[03805184,03805368)`, 484 bytes. The normal computed transfer skips the four-byte `MOV R0,R0` at `038051DC`. The separate scope proof exercises all other 480 bytes, confirming 472 executable bytes outside the configured eight-byte entry. All these bytes were already inside initialized-module coverage, so there is no denominator increase.

The scope proof retains input-module hash `13c0f0469f28daf8fa0921ba61bd78bac7427fb872ef191ba234cd2a73f064d6`, explicit disjoint ARM ranges, computed targets, the skipped NOP and actual native return records. Its 294 standalone original returns validate quotient/remainder words for divisors 1, 5, 7, 100 and 400 over boundary and deterministic full-word inputs. Three separate zero-divisor executions return the incoming numerator in R0 and zero in R1; they do not expand the caller's nonzero-divisor contract. Sixteen scope guards reject namespace, range, target, packed-word, return-count and credit mutations.

This is code-role and ABI evidence, with zero callee-source credit. It does not silently enlarge the canonical function boundary, assign source ownership to a shared tail or prove the absence of opaque outside interior entries. Shared inventory, configuration and denominator remain unchanged for coordinator review. Scope report SHA-256 is `9d1951d47676c59ea4b5c8cdae84150f6d169fbbfda92f3c5467435ebf536e7c`; its 16-control report is `403f55b8b0b071244419dbe797654c31b881a34a22e2ba13d5c0964266b4d48a`.

## Reproduction

```powershell
& C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe C:\Users\trevo\Documents\RecProgramming\DQM\j2p-recovery-lanes\arm7\validate_arm7_lane_child_wordpair124_20261031.py
& C:\Users\trevo\AppData\Local\Programs\Python\Python313\python.exe C:\Users\trevo\Documents\RecProgramming\DQM\j2p-recovery-lanes\arm7\validate_arm7_child_divide_scope_20261031.py
```

The source, prototype history, native/model proof, boundary helper, matcher and controls are frozen for integrator replay. Caller module and whole-ROM source acceptance remain separate gates.
