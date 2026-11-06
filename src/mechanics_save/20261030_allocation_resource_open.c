typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
extern u8 *native_fn_0205db90(void *, const void *, s32);
extern u32 native_fn_0205d9e8(u32, const void *, void *, void *, u32);
extern const u8 native_data_020de42c[];
extern u8 native_data_020db218[];
extern u8 native_data_020db214[];
extern u32 native_data_021c6230;
u32 native_main_020788f0(void) {
    u8 name[32];
    u32 result;
    native_fn_0205db90(name, native_data_020de42c, -1);
    result = native_fn_0205d9e8(1, name, native_data_020db218, native_data_020db214, 1);
    native_data_021c6230 = result;
    return result;
}
