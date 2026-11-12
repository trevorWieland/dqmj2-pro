/* Release the two objects the table at 0x02236f20 still points at.
 *
 * A non-null entry is handed to 0x0202a498 with kind 2 and then cleared. The
 * counter is a signed byte, which is why the loop masks it with 0x18 shifts.
 * Unknowns: what the objects are and why kind 2.
 */
typedef unsigned char u8;
typedef signed char s8;
typedef signed int s32;

extern u8 *native_data_ov000_02236f20[];
extern void native_fn_0202a498(s32, u8 *);

void native_ov000_021f8398(void)
{
    s8 i = 0;

    do {
        u8 *object = native_data_ov000_02236f20[i];

        if (object != 0) {
            native_fn_0202a498(2, object);
            native_data_ov000_02236f20[i] = 0;
        }
        i++;
    } while (i < 2);
}
