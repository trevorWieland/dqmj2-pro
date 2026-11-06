typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
extern s32 native_fn_02026144(s32, s32);
extern u8 *native_fn_0207afec(u32);
extern s32 native_fn_0207b94c(s32, s32);

u32 native_ov001_021efb88(s32 initial_value, u32 action, u8 *actor, u32 control) {
    u8 denominator;
    s32 value;

    value = initial_value;
    if ((((u32) *(u16 *)(native_fn_0207afec(action) + 8) << 0x1C) >> 0x1C) == 1) {
        denominator = actor[0x356];
        if ((u32) denominator > 1U) {
            value = native_fn_02026144(value, (s32) denominator);
            if (value > 2) {
                value += native_fn_0207b94c(4, control) - 1;
                if (value < 0) {
                    value = 0;
                }
            }
        }
    }
    return (u32) value;
}
