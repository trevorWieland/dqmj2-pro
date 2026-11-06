typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern s32 native_fn_0203d294(s32);
extern u8 *native_fn_0207afec(u32);
extern u32 native_fn_0207b004(u32, u32);
extern u32 native_fn_ov001_021ef398(u32, u8 *);
extern u32 native_fn_ov001_02210ba8(u8 *);
u32 native_ov001_021efedc(u32 initial_value, u32 action, u8 *actor, u8 *target) {
    s16 scalar;
    s32 random_word;
    u32 value;

    value = initial_value;
    if (native_fn_0207b004(action, 0x08000000) != 0) {
        if ((native_fn_ov001_02210ba8(target) == 0) && (native_fn_ov001_021ef398(action, target) != 0)) {
            if ((((u32) *(u16 *)(native_fn_0207afec(action) + 8) << 0x1C) >> 0x1C) == 1) {
                if ((((u32) *(u16 *)(native_fn_0207afec(action) + 8) << 0x10) >> 0x1C) == 0) {
                    value = (s32)((u32)value * (u32)0x1B) / 20;
                }
            } else {
                value = (s32)((u32)value * (u32)0xD) / 10;
            }
        }
    } else if ((native_fn_0207b004(action, 1) != 0) && ((((u32) *(u16 *)(native_fn_0207afec(action) + 8) << 0x1C) >> 0x1C) == 1)) {
        if (*(s16 *)(native_fn_0207afec(action) + 0x12) == 0x271C) {
            random_word = native_fn_0203d294(0x15) + 0x14;
            value = (s32)((u32)value * (u32)random_word) / 100;
        } else {
            scalar = *(s16 *)(native_fn_0207afec(action) + 0x12);
            value = (s32)((u32)value * (u32)scalar) / 10;
        }
    }
    return value;
}

