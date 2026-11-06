typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;

extern u32 native_fn_ov001_0220ee3c(u32, u32, u32);

u32 native_ov001_02210748(u8 *skills, u32 action, u32 value) {
    s32 index;
    u8 skill;

    index = 0;
    do {
        skill = skills[index];
        if (skill == 0) {
            break;
        }
        if (skill == 0x11) {
            value = native_fn_ov001_0220ee3c(action, value, 1);
        } else if (skill == 0x12) {
            value = native_fn_ov001_0220ee3c(action, value, 2);
        } else if (skill == 0x13) {
            value = native_fn_ov001_0220ee3c(action, value, 3);
        } else if (skill == 0x14) {
            value = native_fn_ov001_0220ee3c(action, value, 4);
        } else if (skill == 0x15) {
            value = native_fn_ov001_0220ee3c(action, value, 5);
        } else if (skill == 0x16) {
            value = native_fn_ov001_0220ee3c(action, value, 6);
        } else if (skill == 0x46) {
            value = native_fn_ov001_0220ee3c(action, value, 24);
        } else if (skill == 0xFA) {
            value = native_fn_ov001_0220ee3c(action, value, 28);
        }
        index++;
    } while (index < 64);
    return value;
}
