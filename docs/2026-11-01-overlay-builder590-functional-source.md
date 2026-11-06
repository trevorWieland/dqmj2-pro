# 2026-11-01 two nonmatching overlay builders

## Identity and source status

This zero-credit packet covers ARM overlay005 0x021E00D0/412 and overlay006 0x021DE980/284 in ROM SHA-256 674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6. The modules share a load base but are independently loaded and identified by measured hashes. The bodies contain 408+280 instruction bytes and one referenced four-byte global-address literal each. Their new ordinary C drafts are nonmatching: actual MW linkage produces 396/412 bytes with100 equal same-offset bytes for005, and284/284 with135 equal same-offset bytes for006. No source bytes or functions are accepted by this packet.

Run `python prove_overlay_builder590_20261101.py` from the repository or invoke its absolute path from a different working directory. The producer verifies pinned source/model inputs, compiles both larger drafts, genuinely links them with qualified ARM bindings, and separately compiles the exact168-byte main0x02049794 source dependency. It substitutes that newly linked dependency together with the larger candidate. Original runs use the unmodified measured main and overlay code. Compiler work is isolated under work/ol590-proof; no shared builder or registry changes are required.

## Executed behavior

Each module passes80 original/candidate pairs,160 actual top returns. Module005 contributes22542 actual watched dependency returns and5524 provided lower calls; module006 contributes18178 and4438 respectively. Total320 top/40720 dependency returns/9962 provided lower calls. Main49794 returns are already included in the dependency totals; its native getter tail entries are not extra returns. Its168 source bytes add zero credit here.

The VM executes actual signed32 division0x02026144, actual main49794 behavior, and actual native bank/index, counter-getter and counter-update leaves. Only lower0x02049BE4 is provided, with its eleven prepared words captured, no RAM effects, and caller-saved registers/flags poisoned. No resource allocation, rendering or slot-population behavior is supplied as if native.

Independent models validate all RAM effects outside the disposable stack, descriptor fields at offsets0x00/0x04/0x0C/0x0E, complete ten-word calls from the overlay to main49794, complete eleven-word lower calls, bank-wrapped address calculation, counter increments and final module-global stores. Ordered non-stack write address/size/value sequences agree for every pair. All688 original own instruction bytes execute. For each module,64 positive-count cases also match every captured ARM core register and CPSR;16 count0 pairs are only compiled binary evidence outside abstract C division/remainder semantics, with their physical differences retained in full traces. Physical top R0 is recorded as a module-global pointer word, without assigning an original semantic return type to the drafted void view.

Profiles use counts0,1,2,7,127; raw mode words0,1,2,0x80000000; signed totals0,17,-1,INT_MIN; high-bit coordinate/width words; byte wraps; initial counter0xFFFFFFF0; both native bank branches; and supplied empty or occupied slot statuses. Original mode==1 in005 splits each row into two calls; all other raw mode words select one call. Module006 always makes the single-row call and stores zero to its own global. These are bounded synthetic states, not evidence of actual scene entry or legal array dimensions.

## Stack-slot repair and controls

The original006 code consumes incoming SP+0x00, +0x04 and +0x08 as bytes, skips the physical word at+0x0C, and reads the signed division input at+0x10. A weak M2C signature omitted the unused middle position, shifting the final source argument. The new explicit nine-word drafting view preserves the measured physical gap. This is not proof of the game's original formal arity, an invented wide argument, or a value attributed to the skipped word.

Three wrong compiled bodies must actually return before model rejection: replacing remainder with quotient in each module, and dropping the measured stack gap in006. The gap control uses a positive finite count and distinct mode/total words; its failure demonstrates a semantic input-position requirement rather than an allocation-only source perturbation. Earlier experiments remain separate and unmodified.

## Limits and continuation

Counts128..255 and their possible signed-byte counter wrap remain unsupported. Count0 observations do not establish defined abstract C remainder behavior or a legal game input. The actual lower resource constructor, caller scene setup, slot population, asset loading, hardware behavior and the legal bank/index domain remain unresolved. Complete source and native traces are retained in deterministic hashed gzip artifacts, with compact per-case hashes/counts and honest mismatch metadata. The next pass should rotate to another substantial source unit rather than treating these functional drafts as completed source recovery.
