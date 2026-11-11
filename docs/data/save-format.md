# Save format records

Index entries: `save_money`, `save_bank_header`, `saved_record`. Confidence:
**proven-by-code** for every field below; base addresses are **unknown** because the save
buffer is passed as a pointer.

## Money record — `NativeMoney`

| offset | width | type | name | confidence |
| --- | --- | --- | --- | --- |
| 0 | 0x1c | u8[0x1c] | prefix | unknown |
| 0x1c | 4 | s32 (`int`) | gold | proven-by-code |

Evidence: `src/save_accessors.c` declares
`typedef struct { u8 prefix[0x1c]; int gold; } NativeMoney;` and the accessor functions in
the same file are matched. `int` on ARM946E is 32-bit and the accessor compares it as a
signed quantity, hence `s32`.

## Save bank / section header — `NativeSaveBank`

| offset | width | type | name | confidence |
| --- | --- | --- | --- | --- |
| 0x00 | 4 | u32 | marker | proven-by-code |
| 0x04 | 4 | u32 | total_length | proven-by-code |
| 0x08 | 4 | u32 | payload_length | proven-by-code |
| 0x0c | 0x1c | u8[0x1c] | prefix | unknown |
| 0x28 | 4 | u32 | header_word_28 | proven-by-code |
| 0x2c | 0x5c | u8[0x5c] | rest | unknown |
| 0x88 | 4 | u32 | payload_sum | proven-by-code |
| 0x8c | 4 | u32 | header_sum | proven-by-code |

Stride 0x90 (144 bytes). Evidence: `src/save_accessors.c` declares the struct in exactly
this order; the field names above are the struct's own names, so the meaning of
`header_word_28` is **not** claimed beyond "a 32-bit header word at 0x28".

## Saved monster record — `SavedRecord`

| offset | width | type | name | confidence | evidence |
| --- | --- | --- | --- | --- | --- |
| 0 | 24 | u8[24] | prefix | unknown | `src/mechanics_save/20261030_record_descriptor_nibble.c` |
| 24 | 2 | s16 | species | proven-by-code | `src/mechanics_save/20261030_record_descriptor_nibble.c` |

The accessor `native_main_020640b4` fetches a record by id and feeds `record->species`
into the descriptor lookup, which proves the field is a species identifier at offset 24.
Stride 26; record count unknown.

## Related descriptors

`NativeDescriptor { u32 prefix; u16 packed; }` and the save-IO struct
`{ u8 status; signed char heap; u16 reserved; int (*validator)(NativeSaveBank *); u8 *buffer; }`
are also declared in matched files. They are listed here for orientation but not indexed
as tables: they are transient, not stored data.

## Save sections

`src/save_accessors.c` references `native_main`, `native_numeric`, `native_event`,
`native_secondary`, `native_section2`, `native_section3`, `native_section4` and
`native_record_array`. Their **addresses are not established** by matched code, so no
entry with an address exists for them; only the record layouts above are proven.
