# Windows packed word544 - 2026-11-01

Run `python verify_windows_packed_word544_20261101.py`. The two new host ARM7 main ARM functions0x027F6CA0 and0x027F6DB0 compile unchanged as ordinary C for pinned i686 Windows. Their shared unsigned bitfield view occupies four bytes. Every source/header/tool hash is recorded. No original ARM code, ROM or save data enters the PE process; its inputs are synthetic word pages and logical addresses.

There are2,560 unique cases across both functions: every64-code/two-flag combination with eight background words, plus256 additional low-byte planes per function. Each original ARM execution must actually return and pass its independent full-word, read/store, register, stack and memory model. The Windows outputs match all return words and complete4,096-byte pages in two fresh hidden PE32 processes.

Each Windows process additionally executes120 measured no-store cases with the complete input page made read-only. The process must return normally before write access is restored. These cases demonstrate the no-store paths in this pinned Windows build. Windows instruction order, scratch registers, condition flags and concurrency remain unproved; the separate ARM corpus checks its own raw machine behavior.

A complete wrong C source changes flag clearing to setting in the first routine and is separately compiled and executed. All2,560 wrong-process calls return:1,040 reject and1,520 remain unchanged positives, matching the independently predicted branch partition. Both correct Windows runs produce identical bytes. None of this adds decompilation bytes or establishes historical field meanings, ordinary scene reachability, Android bitfield layout, a full Windows game or a source-only ROM.
