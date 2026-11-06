# Overlay005 position/control caller matching source — 2026-10-30

ROM SHA-256 is `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`; ARM9 overlay005 SHA-256 is `efd21cd223735980e3f83f95c796725b0abd677043c40ca26d9762e4ea9a97c8`, base `0x021D7240`. ARM function `0x021DB400` occupies 464 native bytes. “Slider” is an organizational name for its raw offset/position/control-register operations, without assigning game or scene meaning.

Frozen ordinary source is `src/overlays/ov005_20261030_slider20/slider.c`, SHA-256 `0de9c4307e51950c5e416d9dc4f92c159c692c1aebeadcfa0604eaa87b16515d`; header SHA-256 is `5236324b83669ce90aa44cb4f9cb61b8db43ef4dda1ebb5c3945e9d58f696006`. Pinned base MWCC O2/speed, inline off, symbols on matches all 464 compiler/relocation bytes. Genuine pinned MWLD links all 464 identically. Link validation, ELF, control file and caller bytes are captured as immutable generated artifacts.

The compiler recovery uses direct field read/modify/write in the two flag branches, the equivalent increment in the three-row post-test condition and actual volatile hardware-register views. A redundant decompiler temporary declaration is removed without changing linked bytes. No padding, register forcing, fabricated parameters, assembly, byte arrays of executable code or opcode modifications are used. The baseline merged temporary produced an extra pointer reload and 468 bytes; direct field operations restore the native 464-byte structure.

Reproduce from any working directory:

```powershell
python C:\Users\trevo\Documents\RecProgramming\DQM\j2p-recovery-lanes\overlays\match_ov005_slider20_20261030.py
```

The canonical report is `evidence/matches/ov005-20261030-slider20.json`. It records 144 deterministic recipes, 288 actual caller returns and 4,608 original native dependency returns, with zero supplied calls or return stubs. Maximum instruction count is 196 against a 1,000 bound. The original and compiled images agree in all registers, flags, full RAM, RAM-backed I/O, private-stack hashes, PC traces and memory writes. Independent models additionally check complete RAM/I/O and the order and values of native RAM and I/O writes. Full raw traces remain in deterministic hashed gzip.

Inputs cover raw offsets 0, 1, 255, 256, 511, 512, `0xFFFFFFFF`, `0x80000000` and `0x7FFFFFFF`; fields `+0x40` and `+0x68` independently take 0, 1, 2 and `0xFFFFFFFF`. Only equality to 1 selects each corresponding branch. The native low-nine-bit projection is written to registers `0x04000010`, `0x04000014` and `0x0400001C`. The `+0x40 == 1` branch subsequently changes the stored offset to 256 and adjusts control register `0x04000000`. The models preserve this distinction between the earlier register writes and later stored offset. Fixed and three-by-three object position stores and their full-word final R0 pointer are checked independently.

Original main bodies execute at `0x02048A44`, `0x0203515C`, `0x02034D68` and `0x02048A60`. The first chain shifts argument 1 by 13 bits and reaches the real `0x02034D68` guard. Supported object words at its `+0x0C` are 0, 2 and `0xFFFFFFFF`, which execute its actual type-not-1 return. These values live at synthetic object address `0x021E9EB0+0x0C`. The resource-backed type-1 path reaches unmodeled native callee `0x0201AF84` and is retained as an explicit unsupported experiment with no claimed return or source credit. It is never replaced with a stub.

A fresh genuine link of an ordinary C mutation that clears the selected flag instead of setting bit 1 must fail the independent full-RAM/write-order model. This control tests the semantic gate rather than relying on compiler equality. Hardware I/O is isolated RAM, without timing, DMA or display side effects. Synthetic object structures and the guarded dependency path do not establish original asset lifecycle, active SDK behavior or scene reachability.

Normal and alternate-working-directory reports agree completely after excluding only `createdUtc`; deterministic digest is `cc6cfae1965bf4e25112065eae00acc13a10ff08a02579fb91f8b9fb1fc428f3`. Generator SHA-256 is `24c499069aad2129879cda2bac316e8c08ecf184e76257ac17dbb9881792f877`. The full report file hash is a frozen handoff snapshot, not a stable timestamp-bearing replay identity. Integrator replay, registration, module comparison and whole-ROM checks remain necessary for accepted credit. Shared registry/source preferences and application adapters/UI are untouched.
