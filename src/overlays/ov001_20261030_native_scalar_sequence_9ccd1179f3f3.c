typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_020444a8(void);
extern u8 *native_fn_0207afec(u32);
extern u32 native_fn_0207b94c(s32, s32);
extern u32 native_fn_0207b974(u32, u32, u8, s32, s32);
extern s32 native_fn_ov001_021dbcbc(u8 *);
extern s32 native_fn_ov001_021dbd24(u8 *);
extern u32 native_fn_ov001_021dbe68(u8 *);
extern u32 native_fn_ov001_021eeff0(u8, u32);
extern u32 native_fn_ov001_021ef0b0(u8 *, u8 *, u32, s32);
extern u32 native_fn_ov001_021ef224(u8 *, u8 *, u32);
u32 native_ov001_021ef638(u32 value, u32 action, u8 *actor, u8 *target, u32 extra, s32 random_control, s32 double_control, s32 triple_control) {
    u32 mode;
    u32 native_id;
    u32 current;
    u32 maximum;
    u32 random_word;
    u32 basis;
    u8 side;
    mode = ((u32)*(u16 *)(native_fn_0207afec(action) + 8) << 28) >> 28;
    if (mode == 6 || (mode == 5 && (((u32)*(u16 *)(native_fn_0207afec(action) + 8) << 20) >> 28) != 7)) {
        native_id = native_fn_ov001_021eeff0(actor[0x31E], action);
        if (native_id == 0x2714) {
            value += native_fn_ov001_021dbd24(target) / 4;
        } else if (native_id == 0x2715) {
            value += native_fn_ov001_021dbd24(target) / 6;
        } else if (native_id == 0x271B) {
            value += native_fn_ov001_021dbd24(target) / 2;
        } else if (native_id == 0x271D) {
            value += native_fn_ov001_021dbd24(target) / 8;
        } else if (native_id == 0x271E) {
            value += native_fn_ov001_021dbd24(target) / 16;
        } else if (native_id == 0x2716) {
            value += native_fn_ov001_021ef224(actor, target, action);
        } else if (native_id == 0x2717) {
            current = (u32)native_fn_ov001_021dbd24(actor);
            maximum = (u32)native_fn_ov001_021dbcbc(actor);
            random_word = native_fn_0207b94c(6, random_control);
            value += (maximum - current) + (s32)(current * random_word) / 100;
        } else if (native_id == 0x2713) {
            value = (s32)(extra * 3) / 2;
        } else if (native_id == 0x2712) {
            value = native_fn_ov001_021ef0b0(actor, target, action, random_control);
        } else {
            basis = native_fn_ov001_021dbe68(actor);
            if (native_fn_020444a8() != 0) {
                side = 0;
            } else {
                side = actor[0x31E];
            }
            value = native_fn_0207b974(action, basis, side, 0, random_control);
        }
        if (double_control != 0) {
            value *= 2;
        }
        if (triple_control != 0) {
            value = (s32)(value * 3) / 2;
        }
    }
    return value;
}
