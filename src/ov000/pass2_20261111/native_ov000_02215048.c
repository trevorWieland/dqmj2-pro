/* Bounds-checked 12-byte record base.
 *
 * Indexes the 0x300-record table at 0x0222bb18; anything past the end yields the
 * null pointer. The stride is materialised as `mov #12` plus `mla`.
 * Unknowns: the record layout and what the table stores.
 */
typedef unsigned char u8;
typedef unsigned int u32;

extern u8 native_data_ov000_0222bb18[];

u8 *native_ov000_02215048(u32 index)
{
    if (index >= 0x300)
        return 0;
    return native_data_ov000_0222bb18 + index * 12;
}
