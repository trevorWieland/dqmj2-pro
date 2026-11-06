# Cohort 172 unsigned interface repair

The first shared integration attempt rejected a native-symbol collision. The 44-byte GP random-character caller emitted `_s32_div_f` but its measured native call targets the unsigned divider at `02026350`. Its closed header had replaced the primary `sizeof(RANDSTRING)-1` expression with signed `62`.

The separate repair packet restores the actual 63-byte alphabet declaration and unsigned `sizeof` expression. The original C body and all compiler flags remain unchanged; the compiler now emits `_u32_div_f`, and the genuine linked caller matches every original byte. Actual native divider and random-generator executions establish quotient/remainder registers and the random generator's 0–32767 output domain. A wrong-signed control binds to the correct signed divider at `02026144` and fails the native-byte comparison.

The repair preserves all **30 function identities / 8,720 initialized bytes**. Both other GP bodies, all old frozen inputs and the earlier failed transaction remain preserved. Only the failed, unaccepted registry was restored to the exact committed cohort-171 baseline before preparing the replacement transaction. All 11,452 accepted source identities and their hashes were verified. The original collision guard, module builder and sixteen shared validation stages remain unchanged.

- [Lossless failed transaction archive](../evidence/attempts/cohort172-unaccepted-transaction-before-repair-20261106/manifest.json).
- [Baseline restoration](../evidence/verification/cohort172-failed-registry-restored-to-closed171-v1-20261106.json).
- [Unchanged native membership](../evidence/verification/cohort172-unsigned-repair-identical-membership-20261106.json).
- [New frozen repair packet](../evidence/lanes/parallel-wave20261106/gp-core-resume-next/repair/ready.json).
- [Full validation retry](../evidence/verification/cohort172-continuation-driver-v44-20261105.json).

Reference-link controls now also have immutable copied report inputs, including the corrected GP source contract. The supplemental qualification retains all ten genuine positives and 170 negative controls with the same helper implementation. Historical qualification evidence remains preserved. This repair grants no additional coverage; cohort 172 requires completed shared validation and committed closure before acceptance.
