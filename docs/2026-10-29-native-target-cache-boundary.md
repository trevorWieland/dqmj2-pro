# Native target-cache boundary qualification - 2026-10-29

This separate evidence corrects the role assigned to the `02215BC8` boundary without changing the frozen book, item-use or matching-source reports. The authoritative ROM SHA-256 remains `674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6`. The explicitly loaded overlay0 has SHA-256 `783cb72f0d6ee2fdb632aba3e0ae41a9eee0c7e41933192b1680152e50aa61f6`.

Run `python evidence/application/target_cache_boundary_20261029.py`. The report `evidence/application/target-cache-boundary-20261029.json` has SHA-256 `36ef8b4311ae8bd82748cdeb5086c18ec94aff08f6d269fb3513b30e9bc01086`. It records three fresh-machine profiles and 60 top-level actual returns, with native factory returns checked separately. No reconstructed source credit is claimed.

| Qualified native entry | Bytes | Native span SHA-256 | Measured role |
|---|---:|---|---|
| ov000:ARM02215BC8 | 164 | cd0c1a1b8a2e653789d5942f11b96e175f21b90f7dad0b7eb000ff0795c75da2 | Rebuilds six target-cache entries from active/reserve record data |
| ov000:ARM02215C6C | 72 | c9b637772d35ca5aeef6436e1a783c00c62b99a11838cf1130f19224f3b4e3c5 | Builds one entry using record ID lookup and the original two derived helpers |
| ov000:ARM02215D94 | 24 | ee5a8c075fe069f39614a13488cfe590f51bdb6a37dec133385931baa7b2788c | Returns `0224575C + index*100 + 0x20` |

The rebuild first clears each entry's 32-byte prefix at base `0224575C`, stride 100, and byte +0x60. It obtains the native active/reserve counts through main `02062AA0`/`02062AD0`, then supplies each actual record ID to the 72-byte factory in active-then-reserve order. The factory performs original main `02062A10(recordID)` lookup, passes species/variant and record+0x7A into `0207B460`, and writes its 64-byte result to entry+0x20. It then calls `0207B1C4(record+0x7A, entry+0x20, entry)` to build the 32-byte prefix.

The captured profile produces six entries. Their derived 64-byte regions contain respectively 26, 27, 24, 4, 3 and 3 nonzero bytes. Replacing the first record's five-slot profile with `[22,100,0,0,0,0,0,0,0,0]` changes its nonzero count from 26 to 6 while the other five remain unchanged. These are measured bytes, not a complete interpretation of each derived ID or bit.

For every populated entry, separate original `0207B460` and `0207B1C4` controls reproduce both cache regions exactly. The test loads all original overlay0 code and uses no callee providers. Persistent saved-region bytes remain unchanged during cache rebuilding. Bounded hardware division is the only modeled device.

A third profile clears all six active/reserve IDs in disposable memory. No factory call occurs. Every prefix and byte +0x60 is cleared, while the 64-byte feature region and final three bytes retain their prefilled 0xA5 values. Thus inactive derived regions are not fully initialized by the rebuild alone. No validity or status label is assigned to byte +0x60.

The mapper is tested for all indices 0-5 in each profile and returns the precise entry+0x20 pointer without writes. Its index-0 result is `0224577C`, the address used in the direct item-use tests.

The earlier book oracles explicitly substituted `02215BC8` and used zero feature buffers. Their exact compiled source, saved-slot writes, quantity behavior, error cases and declared provider limits remain scoped evidence. They did not establish native cache construction, its nonzero derived contents or resulting future-frame behavior. Any claim that the provider was only presentation would exceed that evidence. The source/byte match and the future cache-state question remain independently reported.

Ordinary UI construction, loaded-overlay selection, bank selection, all other record profiles and independent re-proofs of the two derived formulas remain unsupported. The records are measured from the explicitly copied physical save representation and synthetic variants; no active-bank inference is made. This note and generator leave every previously frozen source and fixture unchanged.
