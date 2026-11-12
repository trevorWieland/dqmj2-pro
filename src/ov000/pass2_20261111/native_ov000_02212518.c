/* Stamp a byte into field 8 of the record found by the lookup.
 *
 * Twin of 0x022124e8 one field further along.
 * Unknowns: what field 8 selects.
 */
typedef unsigned char u8;
typedef signed short s16;
typedef signed int s32;

extern void *native_fn_ov000_02211104(s16, s16);

s32 native_ov000_02212518(s32 x, s32 y, u8 value)
{
    u8 *record = native_fn_ov000_02211104(x, y);

    if (record != 0) {
        record[8] = value;
        return 1;
    }
    return 0;
}
