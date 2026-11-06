typedef unsigned char u8;
typedef signed int s32;
extern const u8 *native_data_021d19e0;
extern s32 native_fn_0209f680(const u8 **);
extern s32 native_fn_0209f6a8(const u8 **);
s32 native_main_0209bbfc(const u8 **output) {
    if (native_data_021d19e0==0) return 0;
    *output=native_data_021d19e0+0x648;
    if (((const volatile u8 *)native_data_021d19e0)[0x38D]==2 || ((const volatile u8 *)native_data_021d19e0)[0x38D]==3)
        return native_fn_0209f6a8(output);
    return native_fn_0209f680(output);
}
