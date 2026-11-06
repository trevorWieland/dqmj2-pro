typedef unsigned char u8;
typedef unsigned int u32;
extern u32 native_fn_020444a8(void);
extern u8 *native_fn_0207afec(u32);
u32 native_ov001_021f08ec(u8 *actor, u32 action) {
    u32 value;
    if (native_fn_020444a8() == 0) {
        if (actor[0x31E] == 0) {
            value = (u32)native_fn_0207afec(action)[0x22] << 28;
        } else {
            value = (u32)native_fn_0207afec(action)[0x22] << 24;
        }
        return value >> 28;
    }
    return ((u32)native_fn_0207afec(action)[0x22] << 28) >> 28;
}
