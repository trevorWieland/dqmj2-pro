/* Byte lookup in the table hanging off 0x022463a0+0xc.
 *
 * The service returns a word handle; its first word is an index into a 7-byte
 * stride table owned by the block. `rsb r0, r0, r0, lsl #3` is the *7.
 * Unknowns: what the handle identifies and what the table's bytes flag.
 */
typedef unsigned char u8;
typedef unsigned int u32;

#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))

extern u8 native_data_ov000_022463a0[];
extern u32 *native_fn_ov000_0221c658(void);

u32 native_ov000_0221f39c(void)
{
    u32 *handle = native_fn_ov000_0221c658();
    u8 *table = M2C_FIELD(native_data_ov000_022463a0, u8 **, 0xc);

    return table[handle[0] * 7];
}
