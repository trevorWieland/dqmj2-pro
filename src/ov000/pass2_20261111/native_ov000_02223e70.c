/* Clear the third 2x3 block of the stride-3 table.
 *
 * Same counter/base order as 0x02223d88 (outer counter first, base in lr, both
 * loops do-while).
 * Unknowns: what the block selects; the twin at 0x02223df0 clears the block
 * immediately before it.
 */
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_ov000_022465a0[];

void native_ov000_02223e70(void)
{
    s8 i = 0;
    s8 j;
    u8 *row = native_data_ov000_022465a0;

    do {
        j = 0;
        do {
            row[j] = 0;
            j++;
        } while (j < 3);
        i++;
        row += 3;
    } while (i < 2);
}
