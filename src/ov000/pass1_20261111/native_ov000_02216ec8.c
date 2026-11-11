/* Gate byte probe and engine query (second query).
 *
 * Sibling of 0x02216ea4 over the same gate byte at 0x0224536c + 16 with
 * native_fn_021fa6b0 as the query.
 * Unknowns: what the gate byte disables and what the query reads.
 */
typedef signed char s8;
typedef unsigned char u8;
typedef unsigned int u32;

extern u8 native_data_ov000_0224536c[];
extern u32 native_fn_021fa6b0(void);

u32 native_ov000_02216ec8(void)
{
    u32 result = 0;

    if (*(s8 *)(native_data_ov000_0224536c + 16) == 0)
        result = native_fn_021fa6b0();
    return result;
}
