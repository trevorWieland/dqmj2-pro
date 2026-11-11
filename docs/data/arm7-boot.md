# ARM7 boot parameters

Index entry: `arm7_boot_parameters`. Confidence: **inferred** (address and size are
measured; the field meanings are not).

| item | value | source of the fact |
| --- | --- | --- |
| module | `arm7-boot` | `public/accepted-data.json` |
| address | `0x02380204` | `public/accepted-data.json` record `arm7-boot/rodata/02380204` |
| size | 24 bytes, all stored | same record (`bytes` = `storedBytes` = 24) |
| kind | `.rodata` | same record |
| declared by | `src/arm7/boot/parameters.c` | same record, `source` field |
| stride | 1 (byte blob) | nothing constrains it; treated as a blob so it can be dumped |
| field meanings | **unknown** | no matched reader decodes these bytes |

The address and extent are measured facts: the typed-data snapshot only admits a record
when it matched and the module linked. The *contents* are not decoded by any matched
function, so the dictionary lists the blob and stops there. A modder can dump it
(`tools/data_dump.py --table arm7_boot_parameters`) and see 24 bytes, but this document
makes no claim about what they mean.
