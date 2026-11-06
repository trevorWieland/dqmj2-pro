# Pure bit accumulator source and ports - 2026-10-31

Main Thumb020A771C/38 now matches every compiled/real-MWLD byte as ordinary C. The prior m2c hypothesis assigned9 after an initial5,while native uses ADD4. The natural compound update +=4 preserves that measured dataflow. Eight bounded operand-order/type/conditional hypotheses remained nonmatching and are retained. No padding,forced register,volatile qualifier or opcode edit is used. The preferred input view is an unsigned32-bit word.

Observed output is5 plus4 for each selected mask2/8 and2 for each selected mask10/20. The result lies among odd values5..17. This numerical behavior is not assigned an original name,format,scene or gameplay meaning. Consumers are not yet fully audited.

The independent native/source matrix uses all256 low-byte values under six upper-word masks:0,FFFF0000,80000000,7FFF0000,55550000,A5A50000. It covers all16 relevant mask combinations and every one of19 native instruction starts. There are1536 pairs/3072 actual top returns in fresh separate Unicorn instances. R0..R12/CPSR,SP/LR/callee restoration and mapped-stack canaries are compared. Any data-memory access fails;none occurs. Exhaustive2^32 execution is not claimed.

Two complete wrong-C bodies change the first weight4to2 or the final mask20to40. Their3072 paired cases/6144 actual returns give1536 independently wrong numeric outputs and1536 observational positives. Register allocation,CPSR differences and instruction scheduling never create semantic rejections. All helper/provider counts remain0.

The same recovered C executes1536 actual public calls in a hidden Windows PE32 process against original native return words. It also builds a freestanding Android23 ARM64 shared object with one exported function and no undefined symbols. Android execution count is0. This is a portable pure-function subset,not whole-game/device/scene proof. Source and pinned tools are explicit;the Windows process receives only deterministic word/return golden data.

Reproduce from any working directory:

`python <repository>/match_mechanics_save_20261031_lane_bit_accumulator.py`

Normal and parent-directory -I -S replays reproduce canonical SHA633599bc127bf41dfc807b1fc2fd2815cb7893c5aaf35bbc03a73f816bee0b16. Current object/link provenance is checked separately from fixed native/source/profile/case identities. Gzip sidecars retain every register/trace case. Root alone performs registration,module/ROM acceptance and source coverage accounting. This candidate adds one function/38 bytes only after those gates;old accepted matches and shared configuration are untouched.
