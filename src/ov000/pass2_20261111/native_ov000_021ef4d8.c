/* Clear flag bit 1 in the six records the pointer table selects, then latch.
 *
 * The table at 0x02236c04 is an array of record pointers; each record keeps a
 * word of control bits at 0x7c. The last store sets word 0xc84 of the block at
 * 0x02101ae8, which is the same latch the twin at 0x021ef57c sets. The image
 * checks the counter after the body, so the scan is a do-while.
 * Unknowns: what bit 1 gates and what the latch triggers.
 */
typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;

#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))

extern u8 *native_data_ov000_02236c04[];
extern u8 native_data_02101ae8[];

void native_ov000_021ef4d8(void)
{
    u8 i = 0;

    do {
        u8 *record = native_data_ov000_02236c04[i];

        M2C_FIELD(record, u32 *, 0x7c) &= ~2;
        i++;
    } while (i < 6);
    M2C_FIELD(native_data_02101ae8, u32 *, 0xc84) = 1;
}
