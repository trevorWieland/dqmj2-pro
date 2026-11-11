/* Byte-state return code.
 *
 * Reads the state byte at 0x02236bc4 and maps it to a small return code: 22 for
 * state 0, 77 for state 1, 78 for anything else. The first test is an
 * early `bxeq` return; the rest is a compare pair with conditional moves.
 * Unknowns: what the state byte means and who consumes the code.
 */
typedef unsigned char u8;
typedef unsigned int u32;

extern u8 native_data_ov000_02236bc4;

u32 native_ov000_021ec748(void)
{
    u32 state = native_data_ov000_02236bc4;

    if (state == 0)
        return 22;
    if (state == 1)
        return 77;
    return 78;
}
