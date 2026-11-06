typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern u8 *native_fn_02065d88(u32);
extern u8 *native_fn_0207afec(u32);
extern u32 native_fn_0207b004(u32, u32);
extern u32 native_fn_0207b02c(u32, u32);
extern u32 native_fn_ov001_021dca60(u8 *);
extern u32 native_fn_ov001_021ef398(u32, u8 *);
u32 native_ov001_021ef8d0(u32 initial_value, s32 action, u8 *actor, u8 *target, s32 control) {
    u32 preceding_eligible;
    u32 value;

    value = initial_value;
    if ((native_fn_0207b02c(action, 0x80000100) == 0) &&
        (((native_fn_02065d88(actor[0x1FD])[0x2D] == 4) &&
        ((action == 0) ||
        (((u32)action - 0xCBU) <= 1U)) &&
        (control == 0)) ||
        (((((u32) *(u16 *)(native_fn_0207afec(action) + 8) << 0x1C) >> 0x1C) == 1) &&
        ((((u32) *(u16 *)(native_fn_0207afec(action) + 8) << 0x10) >> 0x1C) == 1)) ||
        (*(s8 *)(actor + 0x236) != 0))) {
        preceding_eligible = native_fn_ov001_021dca60(target);
        if (native_fn_0207b004(action, 0x08000000) == 0) {
            if (preceding_eligible == 0) {
                value = (s32)((u32)value * (u32)0x5A) / 100;
            } else if (preceding_eligible == 1) {
                value = (s32)((u32)value * (u32)0x32) / 100;
            } else if (preceding_eligible == 2) {
                value = (s32)((u32)value * (u32)0x19) / 100;
            }
        } else if (native_fn_ov001_021ef398(action, target) != 0) {
            if (preceding_eligible == 0) {
                value = (s32)((u32)value * (u32)0x78) / 100;
            } else if (preceding_eligible == 1) {
                value = (s32)((u32)value * (u32)0x46) / 100;
            } else if (preceding_eligible == 2) {
                value = (s32)((u32)value * (u32)0x23) / 100;
            }
        } else {
            if (preceding_eligible == 0) {
                value = (s32)((u32)value * (u32)0x46) / 100;
            } else if (preceding_eligible == 1) {
                value = (s32)((u32)value * (u32)0x23) / 100;
            } else if (preceding_eligible == 2) {
                value = (s32)((u32)value * (u32)0xF) / 100;
            }
        }
    }
    return value;
}
