typedef unsigned char u8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern s32 native_fn_0205cba4(u32, u8 *, s32);
extern u32 native_fn_0205d7cc(u32);
extern u8 *native_fn_020449d4(s32);
extern void native_fn_0205ce38(s32, u32);
extern void native_fn_0205d930(s32, u8 *);
s32 native_ov001_021eec7c(u32 id, u8 *actor, s32 kind) {
    s32 handle;
    s32 category;
    u8 *record;
    u8 *metadata;
    handle = -1;
    if (kind >= 0) {
        handle = native_fn_0205cba4(id, actor, kind);
        if (handle >= 0) {
            if ((native_fn_0205d7cc(id) & 2) ? 1 : 0) {
                record = *(u8 **)(actor + 0x1E8);
                metadata = native_fn_020449d4(*(s16 *)(record + 0x2A));
                category = ((u32)*(u16 *)(metadata + 4) << 20) >> 28;
                if (category == 1) {
                    native_fn_0205ce38(handle, 0x1400);
                } else if (category == 2) {
                    native_fn_0205ce38(handle, 0x1800);
                } else if (category == 3) {
                    native_fn_0205ce38(handle, 0x2000);
                } else if (category == 4) {
                    native_fn_0205ce38(handle, 0x2800);
                } else if (category == 5) {
                    native_fn_0205ce38(handle, 0x3000);
                } else if (category >= 6) {
                    native_fn_0205ce38(handle, 0x4333);
                }
            }
            native_fn_0205d930(handle, actor);
        }
    }
    return handle;
}
