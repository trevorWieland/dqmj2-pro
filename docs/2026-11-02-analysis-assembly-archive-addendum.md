# Analysis assembly archive addendum - 2026-11-02

The large406/416 history collectors looked for `analysis.s`;their workers actually wrote `input.s`. Their claims of complete assembly capture were therefore incomplete. The frozen C,compiler/link comparisons,native-effect reports andallold hashes remain unchanged. This addendum supplies52 exact analysis-assembly files and52 raw job descriptions in a deterministic gzip sidecar. Every assembly's normalized-LF SHA matches its original recorded decompiler-analysis hash;raw byte hashes also preserve original line endings.

Reproduce the self-contained archive check with `python verify_save_core_assembly_archive433_20261102.py`. It reads only committed evidence,not historical work directories. The supplement makes no source orfunction-return claim anddoesnot alter any frozen earlier report. The newer large422 archive includes its actual `input.s` files directly.
