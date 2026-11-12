/* Set or clear bit 1 on the two objects the manager owns.
 *
 * The manager block holds a pointer at +0xc whose 0x1c word is the lookup key
 * passed to 0x0205f98c with the slot index. Slot 0 takes the first argument as
 * its enable flag, slot 1 the second.
 * Unknowns: which objects these are and what bit 1 controls.
 */
typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;

#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))

extern u8 native_data_ov000_022476f0[];
extern u8 *native_fn_0205f98c(u32, u32);

void native_ov000_0222b0c8(s32 first, s32 second)
{
    u8 i = 0;

    do {
        u32 key = M2C_FIELD(M2C_FIELD(native_data_ov000_022476f0, u8 **, 0xc), u32 *, 0x1c);
        u8 *object = native_fn_0205f98c(key, i);
        s32 enable = (i == 0) ? first : second;

        if (enable != 0)
            M2C_FIELD(object, u32 *, 0x7c) |= 2;
        else
            M2C_FIELD(object, u32 *, 0x7c) &= ~2;
        i++;
    } while (i < 2);
}
