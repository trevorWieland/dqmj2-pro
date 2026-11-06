typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
extern s32 native_fn_0203d294(s32);
extern u8 *native_fn_0207afec(u32);
extern u32 native_fn_ov001_021d90c4(u32, s32);
extern s32 native_fn_ov001_021dbd3c(u8 *);
extern u32 native_fn_ov001_021f08ec(u8 *, u32);
u32 native_ov001_021f00c4(s32 value, u8 *attacker, u8 *target, u32 action, s32 control, s32 mode) {
    s32 candidate;
    s32 scaled;
    u32 attribute;
    attribute = native_fn_ov001_021f08ec(target, action);
    if (control != 0 && (mode != 5 || (native_fn_ov001_021d90c4(attribute, 0) == 1 &&
        (((u32)*(u16 *)(native_fn_0207afec(action) + 8) << 28) >> 28) == 1))) {
        s32 attack = native_fn_ov001_021dbd3c(attacker);
        candidate = attack + native_fn_0203d294(attack / 10) - attack / 20;
        if (mode == 7) {
            candidate *= -1;
        }
        scaled = (s32)((u32)value * 12) / 10;
        if (mode != 7) {
            if (candidate <= scaled) {
                candidate = scaled;
            }
            value = candidate;
        } else {
            if (candidate >= scaled) {
                candidate = scaled;
            }
            value = candidate;
        }
    }
    return (u32)value;
}
