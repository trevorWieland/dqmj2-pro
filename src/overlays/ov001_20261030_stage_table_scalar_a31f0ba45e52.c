typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_020444a8(void);
extern u32 native_fn_0207b004(u32, u32);
extern u8 native_data_ov001_0222df40[];
extern u8 native_data_ov001_0222df4c[];
u32 native_ov001_021efbf4(u32 initial_value, u32 action, u8 *actor) {
    u8 factor;
    u32 value;
    s8 stage;

    value = initial_value;
    if ((native_fn_0207b004(action, 0x20000000) != 0) && (stage = *(s8 *)(actor + 0x234), (stage != 0))) {
        if ((actor[0x31E] == 0) || (native_fn_020444a8() != 0)) {
            factor = native_data_ov001_0222df40[stage + 4];
        } else {
            factor = native_data_ov001_0222df4c[stage + 4];
        }
        value = (s32)((u32)value * (u32)factor) / 10;
    }
    return value;
}
