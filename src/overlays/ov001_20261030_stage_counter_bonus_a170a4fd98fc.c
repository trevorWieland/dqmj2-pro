typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_0207b004(u32, u32);
extern u32 native_fn_ov001_02210ba8(u8 *);

u32 native_ov001_021efc7c(u32 initial_value, u32 action, u8 *actor, u8 *target) {
    u8 counter;
    s32 product_word;
    u32 value;
    s8 stage;

    value = initial_value;
    if ((native_fn_0207b004(action, 0x20000000) != 0) && (native_fn_ov001_02210ba8(target) == 0)) {
        stage = *(s8 *)(actor + 0x234);
        if ((s32) stage > 0) {
            counter = actor[0x1FC];
            product_word = stage * ((counter << 0xC) / 5 + 0x1000);
            value += product_word / 4096;
        }
    }
    return value;
}
