# 2026-11-01: Measured pointer-value accesses in nine larger hypotheses

The frozen 285 application queue contained nine C hypotheses that failed compilation because a raw 32-bit address was dereferenced as a scalar. The new 296 pass preserves those originals and introduces explicit access views at measured native load/store sites. All nine alternatives now compile and complete genuine Metrowerks linker comparisons under their prior base and speed profiles: 7,780 native bytes, 18 linked profiles, zero near matches, zero exact matches and zero accepted source bytes.

| Native function | Bytes | Explicit view |
| --- | ---: | --- |
| main ARM 0206E73C | 836 | The raw 61DCC holder result is read as a word-sized pointer. |
| main ARM 020743F8 | 620 | The selected table entry is read as a full word before narrowing; the output and second table use halfwords. |
| main ARM 02080C04 | 1,344 | The full word at global +4 supplies a byte-addressed lookup base. |
| main ARM 02046AF4 | 884 | Input and secondary stream reads use bytes; output-table writes use halfwords at byte offsets. |
| main ARM 02070FD8 | 960 | A descriptor threshold is read through a byte view of the raw helper result. |
| main ARM 0208870C | 704 | A raw ITCM context result supplies a byte argument to the row formatter. |
| main ARM 020BFC04 | 620 | A word pointer at context +8 supplies full-word entries with byte stride 8. |
| main ARM 020C06E8 | 780 | The four-argument compaction hypothesis reads full-word entries with byte stride 16. |
| main ARM 020C0A8C | 1,032 | Selected entries are full-word loads at byte stride 16. |

The selector checks the original instruction bytes and records their addresses, mnemonics and operands. These are observed accesses, not recovered original declarations. The alternatives preserve address arithmetic before adding each typed load/store view. No blind global-width change or blanket parameter rewrite is applied.

Run `python replay_save_core_larger298_20261101.py` from any working directory. The 298 replay consumes the frozen nine source/profile identities, rebuilds all objects and real links locally, and compares the resulting linked executable bytes against their historical hashes. It does not require historical work outputs or rerun the mutable original candidate selection. The same command passed from the lane parent with `-I -S`.

The compact replay report is `evidence/lanes/save-core/larger-replay298-20261101.json`. The original selection and complete compiler provenance remain in `evidence/lanes/save-core/larger-dereferences296-20261101.json` and its deterministic gzip sidecar. Source/object/link provenance is current to each replay; executable-byte identity is checked separately from debug object paths.

These remain nonmatching source hypotheses. Existing selected-C interfaces, escaped stack buffer extents, unused or surplus call arguments, returned raw words, alias domains and ordinary scene prerequisites still require review. In particular, making the 836-byte body compile does not establish the extent of its local destination passed to the halfword fill routine. No native semantic qualification or ordinary preparation behavior is credited by this packet. All previously accepted sources, frozen drafts, application adapters and input files remain unchanged.
