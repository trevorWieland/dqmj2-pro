typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
extern u8 *native_fn_0207afec(u32);
extern u32 native_fn_0207b004(u32, u32);
extern u32 native_fn_ov001_021db9e0(u8 *);

u32 native_ov001_021efcf8(s32 initial_value, u32 action, u8 *actor) {
    u32 category;
    s32 product_word;
    s32 value;

    value = initial_value;
    if (((u32) ((((u32) *(u16 *)(native_fn_0207afec(action) + 8) << 0x1C) >> 0x1C) - 5) <= 1U) && (native_fn_0207b004(action, 0x40000000) == 0)) {
        category = native_fn_ov001_021db9e0(actor);
        if (category == 1) {
            product_word = (s32)((u32)value * 5U);
            value = product_word / 4;
        } else if (category == 2) {
            value = (s32)((u32)value * (u32)0xF) / 10;
        }
    }
    return (u32) value;
}
