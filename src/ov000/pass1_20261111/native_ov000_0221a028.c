/* Live-object flag probe.
 *
 * Loads the pointer at 0x02246044 + 8, rejects the probe when it is null, when
 * bit 1 of its word 6 is not both set, or when its word 3 is neither 0 nor 5.
 * The image materialises the zero result once at the top (r0 = 0) and returns
 * through `bxeq`/`bxne`, so the early outs return the zero-initialised result
 * variable rather than the constant 0.
 * Unknowns: the object's type and what word 3 enumerates.
 */
typedef unsigned char u8;
typedef unsigned int u32;

extern u8 native_data_ov000_02246044[];

u32 native_ov000_0221a028(void)
{
    u32 result = 0;
    u32 *object = *(u32 **)(native_data_ov000_02246044 + 8);

    if (object == 0)
        return result;
    if ((object[6] & 2) != 2)
        return result;
    if (object[3] == 0 || object[3] == 5)
        result = 1;
    return result;
}
