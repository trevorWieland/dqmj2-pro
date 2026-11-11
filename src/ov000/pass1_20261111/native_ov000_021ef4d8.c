/* Bulk gate clear across six objects.
 *
 * Walks the six object pointers in the table at 0x02236c04 and clears bit 1 of
 * each object's word at 0x7c, using a byte-width loop counter (the image masks
 * the incremented counter with 255 and tests at the bottom of the loop).
 * Finally sets the word at native_data_02101ae8 + 0xc84 to 1.
 * Unknowns: which subsystem the six objects belong to; what the trailing word
 * signals.
 */
typedef unsigned char u8;
typedef unsigned int u32;

extern u32 *native_data_ov000_02236c04[6];
extern u8 native_data_02101ae8[];

void native_ov000_021ef4d8(void)
{
    u8 index = 0;

    do {
        u32 *object = native_data_ov000_02236c04[index];

        object[0x7c / 4] &= ~2;
        index++;
    } while (index < 6);
    *(u32 *)(native_data_02101ae8 + 0xc84) = 1;
}
