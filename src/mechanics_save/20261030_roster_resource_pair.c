typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_02044cdc(s32 species);
extern u32 native_fn_0206d3d8(s32 species, u32 flag, u32 offset, s32 option, s32 zero);
extern u32 native_fn_0206d5fc(s32 species, u32 flag, s32 firstOffset, s32 option, s32 zero);
extern u32 native_fn_02072f48(s32 species);
extern u8 native_data_020de25c[];
extern u8 native_data_021c4c08[];
extern u8 native_data_021c4c0c[];
u32 native_main_0206d2e0(s32 arg0, s32 arg1, u32 arg2, u32 arg3, s32 arg4, s32 arg5, s32 arg6) {
    s32 temp_r5;
    s32 temp_r5_2;

    native_fn_02044cdc(arg1);
    if (((s8) *native_data_020de25c != 0) && (native_fn_02072f48(arg1) != 0)) {
        temp_r5 = arg0 * 0x18;
        *(u32 *)(native_data_021c4c08 + temp_r5) = native_fn_0206d3d8(0x9995, arg2, arg3, arg5, arg6);
        *(u32 *)(native_data_021c4c0c + temp_r5) = native_fn_0206d5fc(0x9995, arg2, arg4, arg5, arg6);
    } else {
        temp_r5_2 = arg0 * 0x18;
        *(u32 *)(native_data_021c4c08 + temp_r5_2) = native_fn_0206d3d8(arg1, arg2, arg3, arg5, arg6);
        *(u32 *)(native_data_021c4c0c + temp_r5_2) = native_fn_0206d5fc(arg1, arg2, arg4, arg5, arg6);
    }
    return 0U;
}
