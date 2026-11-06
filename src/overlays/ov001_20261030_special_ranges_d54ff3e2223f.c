typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_0207b94c(s32, s32);
extern u32 native_fn_ov001_021f08ec(u8 *, u32);
extern u32 native_fn_ov001_02209490(u8 *);
u32 native_ov001_021ef0b0(u8 *actor, u8 *target, s32 action, s32 control) {
    s32 random_word;
    s32 factor;
    u32 value = 0;
    native_fn_ov001_02209490(target + 0x22C);
    native_fn_ov001_021f08ec(target, action);
    switch (action) {
    case 0x74:
    case 0x75:
        value = actor[0x1FC] + native_fn_0207b94c(41, control) + 160;
        break;
    case 8:
        value = actor[0x1FC] + native_fn_0207b94c(200, control);
        break;
    case 0x91:
    case 0x92:
    case 0x93:
    case 0xFB:
    case 0x90:
        random_word = native_fn_0207b94c(21, control);
        random_word += 90;
        factor = ((u32)actor[0x1FC] >> 1) + 120;
        value = (s32)((u32)factor * (u32)random_word) / 100;
        break;
    case 0x4E:
        value = native_fn_0207b94c(6, control) + actor[0x1FC] * 2 + 5;
        break;
    case 0x9F:
        value = actor[0x1FC] + native_fn_0207b94c(6, control) + 5;
        break;
    case 0x9E:
        value = actor[0x1FC] + native_fn_0207b94c(4, control);
        break;
    }
    return value;
}
