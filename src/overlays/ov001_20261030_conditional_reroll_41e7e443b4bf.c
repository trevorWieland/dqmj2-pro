typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;

extern s32 native_fn_0203d294(s32);
extern u32 native_fn_0207b674(u32, u8 *);
extern u32 native_fn_0207d988(u32);
extern s32 native_fn_ov001_021dbd24(u8 *);
extern s32 native_fn_ov001_021dbcbc(u8 *);

u32 native_ov001_02210ad0(u8 *actor, s32 limit, s32 threshold) {
    s32 first;
    s32 current;

    first = native_fn_0203d294(limit);
    if (first < threshold) {
        if ((s32)native_fn_0207b674(41, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
            current = native_fn_ov001_021dbd24(actor);
            if ((s32)((u32)native_fn_ov001_021dbcbc(actor) * 3U) <= (s32)((u32)current * 4U)) {
                return native_fn_0203d294(limit) < threshold;
            }
        }
        return 1;
    }
    if ((s32)native_fn_0207b674(40, *(u8 **)(actor + 0x1E8) + 0x46) > 0 || native_fn_0207d988(actor[0x1FD]) != 0) {
        current = native_fn_ov001_021dbd24(actor);
        if (native_fn_ov001_021dbcbc(actor) >= (s32)((u32)current * 4U)) {
            return native_fn_0203d294(limit) < threshold;
        }
    }
    return 0;
}
