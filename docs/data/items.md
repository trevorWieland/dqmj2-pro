# Items

Index entries: `item_descriptors`. Confidence: **proven-by-code** for two field offsets,
**unknown** for the base address and stride.

## Per-item descriptor block

`src/mechanics_save/20261029_item_eligibility.c` (matched, `native_main_02065e44`) obtains
a descriptor by item id and reads two bytes from it:

```c
#define FIELD_AT(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u8 *native_fn_02065d88(int);
...
kind    = FIELD_AT(native_fn_02065d88(item_id), u8 *, 0x28);
subtype = (s32) FIELD_AT(native_fn_02065d88(item_id), u8 *, 0x29);
```

| offset | width | type | name | confidence | evidence |
| --- | --- | --- | --- | --- | --- |
| 0x28 | 1 | u8 | kind | proven-by-code | `src/mechanics_save/20261029_item_eligibility.c` |
| 0x29 | 1 | u8 | subtype | proven-by-code | `src/mechanics_save/20261029_item_eligibility.c` |

Both are read as unsigned bytes (`u8`), so the signedness is proven too: the C code casts
the loaded byte to `u8` before widening for `subtype`.

## Base address and stride

`unknown`. The descriptor is reached only through `native_fn_02065d88(item_id)`, which
takes an item id and returns a byte pointer. No matched code takes the table's address,
so the modder-facing base address is not established and the table is not dumpable. The
one thing that is proven is that descriptors are id-indexed and that at least 0x2a bytes
exist per descriptor.

## What is deliberately absent

Item names, prices, effects, equipment slots and icon ids: no matched reader touches
those offsets, so they are not listed.
