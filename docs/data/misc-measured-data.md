# Measured data blobs

Index entry: `math_table_0x20d3fe0`. Confidence: **inferred** (address, size and stride
are measured; the field meanings are unknown).

| item | value | source of the fact |
| --- | --- | --- |
| module | `main` | `public/accepted-data.json` |
| address | `0x020d3fe0` | `public/accepted-data.json` record `main/data/020d3fe0` |
| size | 16,384 bytes, all stored | same record (`bytes` = `storedBytes` = 16384) |
| kind | `.data` | same record |
| declared by | `generated/math/20261031_sincos_data.c` | same record, `source` field |
| stride | 4 (1,024 records) | chosen only so a modder can page through it |
| field meanings | **unknown** | no matched reader decodes these words |

No matched function reads this region: the typed-data snapshot proves it exists, matched
and linked, at that address and extent, but nothing proves whether the 4-byte words are
fixed-point pairs, tables, or something else. The dictionary therefore documents a blob,
not a field layout, and `public_tools/data_dump.py` dumps the raw words:

```
index,address,raw
0,0x020d3fe0,00000010
1,0x020d3fe4,06000010
2,0x020d3fe8,0d000010
3,0x020d3fec,13000010
```

A future matched reader is what would promote this entry from `inferred`; nothing in this
document guesses at the contents.
