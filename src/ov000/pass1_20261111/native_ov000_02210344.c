/* Stride-708 record byte store.
 *
 * Writes `value` to byte 0x2c1 of record `index` in the table at 0x02238634
 * (records are 708 bytes = 0x2c4) and returns the value zero-extended, which is
 * the `and r0, r1, #255` tail in the image. The record pointer is formed with
 * `mla` and the field offset folds into the store immediate, so the record is
 * addressed through a pointer, not through an array subscript directly in the
 * store expression.
 * Unknowns: the record's remaining layout and the caller's use of the byte.
 */
typedef unsigned char u8;
typedef int s32;
typedef unsigned int u32;

typedef struct {
    u8 body[0x2c1];
    u8 field;
    u8 tail[2];
} Rec708;

extern Rec708 native_data_ov000_02238634[];

u32 native_ov000_02210344(s32 index, u8 value)
{
    Rec708 *record = &native_data_ov000_02238634[index];

    record->field = value;
    return value & 0xff;
}
