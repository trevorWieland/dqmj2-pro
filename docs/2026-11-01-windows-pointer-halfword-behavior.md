# Windows pointer halfword behavior - 2026-11-01

Two explicit pointer-cast variants now execute as ordinary C in a Windows PE32 process. The original accepted ARM sources remain unchanged. Identities are host ARM7 WRAM ARM 0x03801C50 and 0x03801C70; neither address identifies an ARM9 or utility-child routine.

Run `python verify_windows_pointer_halfwords_20261101.py` from any working directory by passing its absolute path. The verifier rechecks both source and candidate hashes against the preserved cast/link proof, uses the measured ARM7 WRAM image, and compiles the candidates and a separate driver with pinned NDK Clang, DLLTOOL and LLD. The executable has an asInvoker manifest and runs hidden with no ROM, ARM instructions or save data supplied to it.

There are 512 deterministic synthetic contexts per routine. Original ARM execution must actually return, preserve SP, callee-save registers and stack guards, make exactly the independently predicted halfword write, and agree with the independently computed return value and complete 4,096-byte data page. Inputs cover bounded negative and positive row/column/index values, low-halfword truncation and sign edges. Out-of-page destinations, misalignment and signed arithmetic overflow are excluded.

Both fresh Windows processes reproduce all 1,024 return values and complete pages exactly. A separately compiled wrong offset in the first routine returns in all contexts, rejects all 512 first-routine contexts and preserves the 512 unchanged second-routine positives. Windows instruction-level store order, ARM scratch registers and flags are not compared. The original ARM ordered-write check is separate.

The evidence is `evidence/portability/pointer-halfwords-windows32-20261101.json`. These are two existing functions with newly tested native variants, so source coverage credit is zero. The other cast variants, hardware, threading, scene integration and a complete Windows game remain unproved.
