typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_ov001_021f0d5c(u32, u8 *, u8 *, u32, s32, u32 *, s32, s32, s32);
u32 native_ov001_021f0030(u32 initial_value, u32 action, u8 *actor, u8 *target, s32 control, u32 *output, s32 modifier_control, s32 feature_a, s32 feature_b) {
    s32 invert_control;

    if (modifier_control == 0) {
        invert_control = 1;
    } else {
        invert_control = 0;
    }
    return native_fn_ov001_021f0d5c(initial_value, actor, target, action, control, output, invert_control, feature_a, feature_b);
}
