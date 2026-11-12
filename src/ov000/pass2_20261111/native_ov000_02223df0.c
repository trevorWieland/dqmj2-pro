/* Clear the second 2x3 block of the stride-3 table.
 *
 * Same counter/base order as 0x02223d88 (outer counter first, base in lr, both
 * loops do-while).
 * Unknowns: what the block selects; why this table starts six bytes into the
 * one at 0x02246594.
 */
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_ov000_0224659a[];

void native_ov000_02223df0(void)
{
    s8 i = 0;
    s8 j;
    u8 *row = native_data_ov000_0224659a;

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
