typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_02044cdc(s32 species);
extern u32 native_fn_0203d128(void);
u32 native_main_02072f48(s32 species) {
    u32 result = 0;
    if (native_fn_02044cdc(species) != 2) {
        goto done;
    }
    if (native_fn_0203d128() != 0) {
        goto done;
    }
    result = 1;
done:
    return result;
}
