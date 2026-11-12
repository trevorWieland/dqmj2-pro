/* Stamp a byte into field 0xc of the record found by the lookup.
 *
 * Twin of 0x02212480 with the field twelve bytes into the record.
 * Unknowns: what field 0xc selects.
 */
typedef unsigned char u8;
typedef signed short s16;
typedef signed int s32;

extern void *native_fn_ov000_02211104(s16, s16);

s32 native_ov000_022124b4(s32 x, s32 y, u8 value)
{
    s32 result = 0;
    u8 *record = native_fn_ov000_02211104(x, y);

    if (record != 0) {
        result = 1;
        record[0xc] = value;
    }
    return result;
}
