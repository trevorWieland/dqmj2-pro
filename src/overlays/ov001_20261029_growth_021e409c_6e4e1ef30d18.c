typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_fn_ov001_021e404c();
extern u32 native_fn_ov001_021e8e08();
u32 native_ov001_021e409c(s32 arg0, s32 arg1, u32 arg2, u32 arg3, s32 arg4, s32 arg5, s32 arg6) {
    s32 rounding_input;
    s16 parent_gain;

    parent_gain = 0;
    if (arg0 != 0) {
        parent_gain += native_fn_ov001_021e404c(arg2, native_fn_ov001_021e8e08(arg4, arg6));
    }
    if (arg1 != 0) {
        parent_gain += native_fn_ov001_021e404c(arg3, native_fn_ov001_021e8e08(arg5, arg6));
    }
    rounding_input = parent_gain + 3;
    return (u32)(s16)((rounding_input)/4);
}
