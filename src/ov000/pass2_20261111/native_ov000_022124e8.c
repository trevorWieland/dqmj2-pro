/* Stamp a byte into the record found by the signed-coordinate lookup.
 *
 * Both coordinates are sign-extended halfwords; the lookup returns a record or
 * null, and only a hit writes field 7 and reports success.
 * Unknowns: what field 7 selects and which record family the lookup walks.
 */
typedef unsigned char u8;
typedef signed short s16;
typedef signed int s32;

extern void *native_fn_ov000_02211104(s16, s16);

s32 native_ov000_022124e8(s32 x, s32 y, u8 value)
{
    u8 *record = native_fn_ov000_02211104(x, y);

    if (record != 0) {
        record[7] = value;
        return 1;
    }
    return 0;
}
