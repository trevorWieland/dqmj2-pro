typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_020211e8(u32, s32, const u16 *, const u32 *);
u32 native_main_020211c0(u32 buffer, s32 limit, const u16 *format, ...) {
    u32 arguments = (u32)&format;
    arguments &= ~3U;
    arguments += 4;
    return native_fn_020211e8(buffer, limit, format, (const u32 *)arguments);
}
