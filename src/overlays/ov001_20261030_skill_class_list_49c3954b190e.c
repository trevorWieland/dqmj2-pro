typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

extern u32 native_fn_02044cdc(s32);

u32 native_ov001_02210888(u8 *actor, u8 *target, s32 value) {
    u32 classification;
    s32 index;
    u8 skill;

    index = 0;
    do {
        skill = (*(u8 **)(actor + 0x1E8) + index)[0x46];
        if (skill == 0) {
            break;
        }
        if (skill == 31) {
            classification = native_fn_02044cdc(*(s16 *)(*(u8 **)(target + 0x1E8) + 0x2A));
            if (classification == 1) {
                value = (s32)((u32)value * 5U) / 4;
            } else if (classification == 2) {
                value = (s32)((u32)value * 3U) / 2;
            }
        }
        if (skill == 32 && native_fn_02044cdc(*(s16 *)(*(u8 **)(target + 0x1E8) + 0x2A)) == 0) {
            value = (s32)((u32)value * 12U) / 10;
        }
        index++;
    } while (index < 64);
    return (u32)value;
}
