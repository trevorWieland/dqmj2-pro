/* Bulk gate clear across six objects (second table).
 *
 * Identical shape to 0x21ef4d8 with the object pointer table at 0x02236bec.
 * Clears bit 1 of each object's word at 0x7c and sets the word at
 * native_data_02101ae8 + 0xc84 to 1.
 * Unknowns: which subsystem the six objects belong to; what the trailing word
 * signals.
 */
typedef unsigned char u8;
typedef unsigned int u32;

extern u32 *native_data_ov000_02236bec[6];
extern u8 native_data_02101ae8[];

void native_ov000_021ef57c(void)
{
    u8 index = 0;

    do {
        u32 *object = native_data_ov000_02236bec[index];

        object[0x7c / 4] &= ~2;
        index++;
    } while (index < 6);
    *(u32 *)(native_data_02101ae8 + 0xc84) = 1;
}
