/* Clear flag bit 1 in the six records of the second pointer table, then latch.
 *
 * Twin of 0x021ef4d8; the pointer table at 0x02236bec is ten bytes before the
 * first one's, and the same 0x02101ae8 latch is set afterwards.
 * Unknowns: the two tables' owners and what makes them distinct.
 */
typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;

#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))

extern u8 *native_data_ov000_02236bec[];
extern u8 native_data_02101ae8[];

void native_ov000_021ef57c(void)
{
    u8 i = 0;

    do {
        u8 *record = native_data_ov000_02236bec[i];

        M2C_FIELD(record, u32 *, 0x7c) &= ~2;
        i++;
    } while (i < 6);
    M2C_FIELD(native_data_02101ae8, u32 *, 0xc84) = 1;
}
