/* Fill the first 2x3 block of the stride-3 table with ones.
 *
 * The image initialises the outer counter before loading the row base, keeps the
 * base in lr, the outer counter in r3 and the inner counter in ip; both levels
 * are do-while.
 * Unknowns: what the block gates; the table's extent beyond the six bytes touched.
 */
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_ov000_02246594[];

void native_ov000_02223d88(void)
{
    s8 i = 0;
    s8 j;
    u8 *row = native_data_ov000_02246594;

    do {
        j = 0;
        do {
            row[j] = 1;
            j++;
        } while (j < 3);
        i++;
        row += 3;
    } while (i < 2);
}
