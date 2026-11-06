typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
extern u8 *native_fn_0207afec(u32);
extern u8 native_fn_ov001_021d908c(u32, u32, s32);
extern u8 native_fn_ov001_021d90c4(u32, s32);
extern u32 native_fn_ov001_021f08ec(u8 *, u32);
extern u32 native_fn_ov001_021f0d10(u8 *, u8 *, u32, s32);
extern s32 native_fn_ov001_02209490(u8 *);
extern u32 native_fn_ov001_02210ad0(u8 *, s32, s32);
u32 native_ov001_021f0d5c(u32 initial_value, u8 *actor, u8 *target, u32 action, s32 control, u32 *output, s32 modifier_control, s32 feature_a, s32 feature_b) {
    u32 classification_word;
    u32 tier;
    u32 attribute;
    s32 coefficient;
    s32 fixed_sign = 0;
    u32 *status_output;
    u32 value;
    u32 local_status;
    u32 classification;

    status_output = output;
    value = initial_value;
    if (status_output == 0) {
        status_output = &local_status;
    }
    *status_output = 0U;
    native_fn_0207afec(action);
    if ((s32) native_fn_0207afec(action)[0x1F] > 0) {
        attribute = native_fn_ov001_021f08ec(target, action);
        coefficient = native_fn_ov001_02209490(target + 0x22C);
        tier = native_fn_ov001_021f0d10(actor, target, action, modifier_control);
        classification_word = native_fn_ov001_021d90c4(attribute, coefficient);
        classification = classification_word;
        if (classification_word == 1) {
            if ((feature_a == 0) && (feature_b == 0)) {

            } else if ((s32) tier <= 4) {
                tier = 0;
            }
        }
        coefficient = native_fn_ov001_021d908c(attribute, tier, coefficient);
        if (classification == 0) {
            value = (s32)((u32)value * (u32)coefficient) / 100;
        } else if ((((u32) *(u16 *)(native_fn_0207afec(action) + 8) << 0x1C) >> 0x1C) != 1) {
            if ((native_fn_ov001_02210ad0(actor, 0x64, coefficient) == 0) && (control == 0)) {
                value = 0;
            }
        } else {
            fixed_sign = 1;
        }
        if ((tier == 7) && (fixed_sign == 0)) {
            value *= -1;
        }
        *status_output = tier;
    }
    return value;
}
