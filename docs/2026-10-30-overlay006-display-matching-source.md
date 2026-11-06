# Overlay006 display caller matching source — 2026-10-30

ROM SHA-256 is `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`. ARM9 overlay006 is independently identified by SHA-256 `fb9cb28ea400207bda442e3265da73af994866cf3a6c352b46a11db59835d341`, base `0x021D7240`. ARM function `0x021DB050` occupies 812 native bytes. The name “display caller” describes its supplied text/label service protocol and does not establish a particular menu or game statistic.

The frozen ordinary C source is `src/overlays/ov006_20261030_display17/display.c`, SHA-256 `25c1000301410c5a92d3e371f1d64227c96a174a21fe87a870c473d31b847c56`. Header SHA-256 is `fcd47e23978a6ec1d5fecedbd03dca92f3d0013d7902833f643de9a2b1d2d6ff`. Pinned base MWCC at O2/speed, inline off and symbols on matches the complete compiled span and ELF relocations. Genuine pinned MWLD links all 812 bytes identically; immutable linker/ELF/control-file/caller snapshots are retained by the canonical producer.

The breadth draft's scalar `sp8` represented a 64-byte text output within a native 72-byte local allocation. Replacing that scalar with `u16 text[32]` produces the correct frame and 797 equal linked bytes. Moving the four-row counter increment into the post-tested condition gives 810. Viewing the actual row-base result of `main/0x02067A30` as a byte pointer closes the final two operand-order bytes without changing the arithmetic. These are three bounded ordinary C trials; no invented padding, forced register, extra parameter, assembly or opcode patch is present.

The getter qualification matters: `0x02067A30` loads root literal `0x021C3708`, then loads R0 from root `+0x30`. It is not a direct literal return. `0x020679F0` similarly reads root `+0x2C`. Those pointees are runtime inputs, explicitly initialized in the isolated fixtures. The byte pointer view follows the actual caller's four records, 20-byte stride and word read at record `+0x10`; no live value or game meaning is inferred. The earlier tuning description calling this a literal getter was corrected before the canonical proof; source bytes were unaffected.

Run from any working directory:

```powershell
python C:\Users\trevo\Documents\RecProgramming\DQM\j2p-recovery-lanes\overlays\match_ov006_display17_20261030.py
```

`evidence/matches/ov006-20261030-display17.json` records 56 deterministic recipes, 112 actual caller returns, 1,856 original native dependency returns and 3,216 separately supplied service calls. Maximum native instruction count is 263 against a 2,000 bound. Normal and alternate-working-directory reports agree completely after excluding only `createdUtc`; deterministic digest is `6b1678419cb4ef0c163b2a0f693d17fbf8230cc0fdd155911d0b7a83ebf59749`. Generator SHA-256 is `ecf0a2a78ce2e3ebb7074ae880f6967fa688aceae66f9cc278a12dcb036afff9`. Full recipe/register/memory-write/PC traces are retained in deterministic hashed gzip.

Original main bodies execute for `0x02067748`, `0x0206442C`, `0x020643FC`, `0x020679F0` and `0x02067A30`. Identifier inputs cover 0, 1, 46, 47, 239, 240 and 65535. The original `0x020643FC` behavior is modeled independently as 0→0, 1..46→1 and 47..65535→`(identifier-46)&0xFFFF`; this is a raw transformation, not evidence that every supplied identifier is valid in the game. Word inputs include zero, all ones, signed boundaries and wrapped sums/differences. Both zero/nonzero display branches and text lengths 0, 1 and 31 are exercised.

Each original and reconstructed run has a fresh ARM946 machine, seeded scratch/preserved registers, flags, RAM and private stack. Independent models check every supplied argument, the low-halfword field projection, two word sums/difference, four-row sum, output buffers, physical final R0, true return, stack restoration and preserved registers. Because the complete caller image is identical, all registers, flags, full RAM, private-stack hashes, instruction traces and writes also compare exactly. A fresh genuine link of the original scalar-buffer draft must fail the output allocation gate before the provider writes a complete payload.

Formatting, number conversion, labels, cache/preparation and display services are explicit supplied contracts. Their opaque 16-bit output words do not establish font encoding, historical formatting or rendered pixels. Pointee structures are synthetic mapped inputs; valid original resources, save state, scene reachability, malformed/unmapped pointers, lower error paths and hardware timing remain unsupported. The final full-word R0 is physical forwarding of the supplied final service result, with no semantic return name. Supplied services receive zero native/source credit.

This lane supplies a byte-exact source candidate and bounded semantic evidence. Integrator replay, source registration, affected module links and whole-ROM gates remain necessary for accepted credit. The lane does not edit the shared registry, preferences or application adapters/UI.
