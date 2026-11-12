typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed char s8;
typedef signed short s16;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))
/* Forward a slot's object to two consumers, with a compound null test.
 * 
 * `slot` is the address returned by the first service; `*slot` is the object whose
 * +4 word is passed on. The image re-dereferences `*slot` for the second call, so
 * the source does too. `cmpne` shows the two null tests are one compound condition.
 * Unknowns: what the object's +4 word is and what the consumers do with it. */

extern u32 *native_fn_02049ad0(u32);
extern void native_fn_020852c8(u32, u32);
extern void native_fn_02086b14(u32, u32);

void native_ov000_021f02b4(u32 a, u32 b)
{
    u32 **slot = (u32 **)native_fn_02049ad0(a);

    if (slot == 0 || *slot == 0)
        return;
    native_fn_020852c8((*slot)[1], b);
    native_fn_02086b14((*slot)[1], 0x10);
}
