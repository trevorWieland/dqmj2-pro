/* Forward four caller words plus four bytes and three derived stack words.
 *
 * The image reads the four byte arguments from the caller's stack frame, widens
 * the first three unsigned and the fourth signed, and appends the signed byte at
 * 0x0224536c+0x10, then 4 and 5. The first four register arguments pass straight
 * through.
 * Unknowns: what 0x020499a8 does with the ten values.
 */
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;

#define M2C_FIELD(value, type, offset) (*(type)((u8 *)(value) + (offset)))

extern u8 native_data_ov000_0224536c[];
extern void native_fn_020499a8(u32, u32, u32, u32, u32, u32, u32, u32,
                               s32, u32, u32);

void native_ov000_02216350(u32 arg0, u32 arg1, u32 arg2, u32 arg3,
                           u8 arg4, u8 arg5, u8 arg6, s8 arg7)
{
    native_fn_020499a8(arg0, arg1, arg2, arg3, arg4, arg5, arg6, arg7,
                       M2C_FIELD(native_data_ov000_0224536c, s8 *, 0x10), 4, 5);
}
