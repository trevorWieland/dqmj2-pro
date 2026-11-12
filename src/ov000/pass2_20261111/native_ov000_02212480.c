/* Stamp a byte into field 9 of the record found by the lookup.
 *
 * The result is declared first so the image keeps it in r4 and the value
 * argument in r5 across the call, which is why the prologue saves three
 * registers. It starts at zero, is set on a hit and moved into r0 once.
 * Unknowns: what field 9 selects.
 */
typedef unsigned char u8;
typedef signed short s16;
typedef signed int s32;

extern void *native_fn_ov000_02211104(s16, s16);

s32 native_ov000_02212480(s32 x, s32 y, u8 value)
{
    s32 result = 0;
    u8 *record = native_fn_ov000_02211104(x, y);

    if (record != 0) {
        result = 1;
        record[9] = value;
    }
    return result;
}
