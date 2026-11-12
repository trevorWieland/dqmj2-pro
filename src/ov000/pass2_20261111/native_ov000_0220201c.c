/* Submit the pair indexed by (index + 1) to the request service.
 *
 * The pair comes from the first two halfwords of 0x0222b9f0; the request id is
 * the literal 1 while the same (index + 1) halfword goes on the stack as the
 * first stack argument. The kind words are 5 and 0 and the two trailing stack
 * words are 1, which the image materialises once in r0.
 * Unknowns: what request 1 means and what the pair selects.
 */
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;

#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))

extern u8 native_data_ov000_0222b9f0[];
extern void native_fn_0204a574(u32, u16 *, u32, u32, u32, u32, u32);

void native_ov000_0220201c(u16 index)
{
    u16 pair[2];
    u16 value = index + 1;

    pair[1] = M2C_FIELD(native_data_ov000_0222b9f0, u16 *, 2);
    pair[0] = M2C_FIELD(native_data_ov000_0222b9f0, u16 *, 0);
    native_fn_0204a574(1, pair, 5, 0, value, 1, 1);
}
