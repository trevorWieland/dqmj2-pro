These four files preserve the exact Python verification sources pinned by historical cohort 175 packet evidence. Their hashes and original paths are recorded in `public/frozen-validation/cohort175.json`.

They are not on the normal CI module search path. Matching CI uses the current public tooling and freshly compiles and links the accepted C sources. Historical packet analysis requires explicitly selecting its archived module versions; the archive does not claim that an old command runs unchanged in the current checkout.

No compiler C/header input or normal closure runtime pin is redirected. The private input bundle supplies neither version of these public Python sources.
