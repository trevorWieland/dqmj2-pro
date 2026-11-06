typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_0202b044(u32 heap, u32 bytes, s32 alignment);
extern u32 native_fn_0202b0f8(u32 heap, u32 bytes, s32 alignment);

u32 native_main_0202b334(u32 heap, u32 bytes, s32 alignment) {
    if (bytes == 0) bytes = 1;
    bytes = (bytes + 3) & ~3U;
    if (alignment >= 0) {
        return native_fn_0202b044(heap, bytes, alignment);
    }
    return native_fn_0202b0f8(heap, bytes, (s32)(0U - (u32)alignment));
}
