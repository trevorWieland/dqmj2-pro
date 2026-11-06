typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_0207b004(u32, u32);

u32 native_ov001_021f040c(u32 initial_value, u32 action, u8 *actor) {
    u32 value;

    value = initial_value;
    if ((native_fn_0207b004(action, 0x800000) != 0) && (*(s8 *)(actor + 0x234) == 4)) {
        value = (s32)((u32)value * (u32)7) / 10;
    }
    return value;
}
