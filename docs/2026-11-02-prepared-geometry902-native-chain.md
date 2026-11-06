# Prepared geometry query, 2026-11-02

ROM674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6, ARM9 overlay000 ARM0x021DBC18/1884. Replay: `python prove_ov000_geometry902_20261102.py`.

This uses unchanged readable876 C at genuine private origin0x02650000, with three separately linked whole-C controls. Canonical output remains1272 versus1884 bytes: zero source, function, module or ROM completion credit. Objects, relocations, anchors, linker controls and pinned compiler/linker identities are retained.

All758 original/C pairs pass:1516 actual top returns,9002 actual native helper returns,0 supplied function calls,385 hit pairs and373 miss pairs. Three controls properly return758 times each, rejecting758/367/399 scenarios. Full observable8MiB RAM outside measured private-stack union, ordered writes, relevant call words/returns and full4KiB modeled MMIO state agree. Raw scratch/CPSR/LR differences remain in deterministic compressed traces. Different-directory `python -I -S` replay yields identical report/trace hashes.

Original0x021DBBB8 ->0x021DBB50 ->0x021DB968 preparation and0x021DA57C hit notification execute, alongside original main0x0200235C/2458/23C4 division instructions. Preparation overwrites the poisoned prior count before eligibility: two SH writes at context+0x12 and one u8 count write at+0x11. The argument-home write at incoming SP is independently checked. Hit notification writes u8 at+0x00/+0x01 and u32 at+0x04/+0x08/+0x0C. All256 raw capacity bytes and four initial index-word upper halves are tested with low16 zero. BB50 R3 remains a physical spacer, with no original formal-arity claim.

Inputs are supplied one-record/one-block meshes with three negative adjacency halfwords, bounded horizontal/tilted Q12 planes, flags and optional output. The unchanged Root MMIO backend supports only numerator>=0/denominator>0. Arbitrary graphs/multiple candidates, signed-negative or zero divisors, latency/device coherence and ordinary scene reachability stay unproved. Zero function providers does not mean actual hardware execution. No record33 or game meaning is inferred.

Two rejected model attempts are preserved: omitted incoming argument-home write, then tuple-versus-list trace encoding. Corrected checks preserve native execution. Frozen874/877/881 and all accepted helpers remain unchanged.
