typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_02049aa8(u32);
extern u32 native_fn_02049f4c(void **);
extern void native_fn_02048f9c(u32);
extern u32 native_fn_02087a48(u32, u32, s32, s32, s32, s32);

u32 native_main_0204a104(u32 first, const s16 *coordinates, s32 word4, s32 word5) {
    u32 word;
    void **holder;
    holder = (void **)native_fn_02049aa8(first);
    word = ((const u32 *)*holder)[1];
    native_fn_02049f4c(holder);
    native_fn_02048f9c(1);
    return native_fn_02087a48(word, 0, coordinates[0], coordinates[1], word4, word5);
}
