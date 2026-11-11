/* State byte to argument mapping and tail call.
 *
 * Reads the state byte at 0x02236bc4, maps 0 to 16, 1 to 75 and anything else to
 * 76, and tail-calls native_fn_02063b18 with that value. mwcc lowers the return
 * of a call into `ldr r12, =callee` plus `bx r12`, so the row is a plain return
 * of the callee's value.
 * Unknowns: what the callee does with the mapped code.
 */
typedef unsigned char u8;
typedef unsigned int u32;

extern u8 native_data_ov000_02236bc4;
extern u32 native_fn_02063b18(u32);

u32 native_ov000_021ec718(void)
{
    u32 state = native_data_ov000_02236bc4;
    u32 code;

    if (state == 0)
        code = 16;
    else if (state == 1)
        code = 75;
    else
        code = 76;
    return native_fn_02063b18(code);
}
