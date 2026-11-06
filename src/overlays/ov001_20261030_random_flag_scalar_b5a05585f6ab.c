typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
extern s32 native_fn_0203d294(s32);
extern u32 native_fn_0207b004(u32, u32);

u32 native_ov001_021ef878(u32 initial_value, u32 action, u8 *actor) {
    s32 random_factor;
    u32 value;

    value = initial_value;
    if ((native_fn_0207b004(action, 0x80) != 0) && (*(s8 *)(actor + 0x246) != 0)) {
        random_factor = native_fn_0203d294(6) + 0x14;
        value = (s32)((u32)value * (u32)random_factor) / 10;
    }
    return value;
}
