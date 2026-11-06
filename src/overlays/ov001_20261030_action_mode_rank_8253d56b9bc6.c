typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;
extern u8 *native_fn_0207afec(u32);
extern u32 native_fn_ov001_021f0ca0(u8 *, u8 *, s32, s32, s32);
u32 native_ov001_021f0d10(u8 *actor, u8 *target, u32 action, s32 modifier_control) {
    u8 primary_mode;
    u8 secondary_mode;

    primary_mode = native_fn_0207afec(action)[0x1F];
    secondary_mode = native_fn_0207afec(action)[0x20];
    return native_fn_ov001_021f0ca0(actor, target, (s32) primary_mode, (s32) secondary_mode, modifier_control);
}
