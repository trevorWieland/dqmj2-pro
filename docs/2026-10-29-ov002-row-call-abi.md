# Ov002 row orchestration and call ABI, 2026-10-29

The measured ROM is SHA-256 674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6. Overlay002:ARM 021D7F98..021D8094 is 252 B. `src/overlays/ov002_20261029_rows.c` now matches the full native span using the pinned MW 2.0/SP1p5 compiler with its recorded O2/speed configuration and the verified real linker. The exact source report is `evidence/matches/ov002-20261029-rows.json`; replay `python match_ov002_rows_20261029.py`.

An initialized loop-counter comparison against the unsigned bound reproduces the native lower-or-same zero gate. The previous count-greater-than-zero condition emitted a different branch byte. The counter is eight bits; count 256 therefore wraps indefinitely. This is preserved, not silently repaired.

Sixty-four vectors/128 actual returns cover counts 0/1/2/6/127/128/250/255 and eight boundary argument/field patterns. An independent word-level model checks both native callee call contracts, including register and stack arguments. Two count 256 runs stop at the same 20,000 instruction cap and receive zero return credit. RAM, stack/register/CPSR effects and store/PC traces agree. The two native callee boundaries use explicit return-only providers; native UI execution and scene reachability are not certified by this test.

Caller arguments are promoted full words. Narrower inferred callee declarations changed caller bytes, even though separate already-matched callee bodies had compiled from narrow views. The caller therefore records an explicit word ABI, including the modulo-byte cast following the defined unsigned arg5+2 calculation. This does not establish universally consistent original C headers or justify changing frozen callee source. A matching callee body alone does not prove its complete caller-facing signature.

The full module gate accepted this 252 B source range in cohort 41. Five other ov002 functions and module metadata remain unresolved; standalone near-matches receive zero exact credit. No assembly, postlink byte patch, executable byte array, application edit or original-input mutation is used.
