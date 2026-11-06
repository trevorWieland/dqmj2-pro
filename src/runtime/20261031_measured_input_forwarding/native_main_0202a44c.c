typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_0202a37c(u32 heap, u32 bytes, s32 alignment);
extern u32 native_fn_02008d78(u32 pointer, u32 value, u32 bytes);

u32 native_main_0202a44c(u32 heap, u32 bytes, s32 alignment) {
    u32 result = native_fn_0202a37c(heap, bytes, alignment);
    if (result != 0) {
        native_fn_02008d78(result, 0, bytes);
    }
    return result;
}
