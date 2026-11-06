# 2026-11-01: Research transport and actual replay reads

The frozen111-file preparation318 manifest overincluded historical generated reports from its275 dependency packet. Root correctly rejected an already regenerated constructor270 report whose current provenance differs. No file was overwritten, and no source or native-case mismatch occurred.

A new Python read audit executes all three unchanged318 producers. It confirms that no historical constructor270, preview271 or other275 generated report is read. The preexisting report inputs are only the new299/300/303 compiler archives; a current301 sidecar is read after being produced. Project and seed-manifest inputs remain pinned. Native compiler/linker file access is outside the Python audit, so source/header/runtime provenance remains independently pinned as before.

The new transport320 retains every code/source/header dependency and each new318 report/sidecar. It omits historical generated report/sidecar entries already preserved in the original frozen manifest and Git commit. The111-file original, all original hashes, all source/native identities, all case gates and all replay code stay unchanged. Run the unchanged318 replay. This is a transport correction and adds no reconstructed bytes or functions.

The same source-only transport convention is applied prospectively in321 to the frozen319 breadth packet: keep code, new corpus evidence, its exact source/profile archives and generated315 failure evidence, while excluding old285 derived reports and sidecars. The unchanged319 replay consumes the new314/315/316 corpora, materializes its objects locally, and requires no old285 generated report. Original380-path manifest remains immutable archival provenance.
