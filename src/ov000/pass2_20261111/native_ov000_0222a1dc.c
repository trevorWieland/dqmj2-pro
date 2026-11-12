/* Search a -1-terminated halfword list for a value.
 *
 * The list pointer lives at offset 8 of the block at 0x0224754c. The image
 * compares the value before testing the terminator on every iteration, so the
 * loop is a do-while whose sentinel test runs after the increment. The index is
 * declared before the list pointer: that order is what puts the index in r3 and
 * the list in ip.
 * Unknowns: what the list identifies and whether it can be empty.
 */
typedef unsigned char u8;
typedef signed short s16;
typedef signed int s32;

#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))

extern u8 native_data_ov000_0224754c[];

s32 native_ov000_0222a1dc(s32 value)
{
    s32 i = 0;
    s16 *list = M2C_FIELD(native_data_ov000_0224754c, s16 **, 8);

    do {
        if (list[i] == value)
            return 1;
        i++;
    } while (list[i] != -1);
    return 0;
}
