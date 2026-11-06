typedef unsigned char u8;
typedef unsigned int u32;
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
typedef struct {
    u8 unknown_0[0x30];
    u32 field_30;
} Record_native_data_020e33c0;
extern Record_native_data_020e33c0 native_data_020e33c0;
u32 native_main_02006c38(u32 arg0) {
    u32 temp_r0;
    u32 temp_r4;

    temp_r0 = native_fn_02007ff4();
    temp_r4 = native_data_020e33c0.field_30;
    native_data_020e33c0.field_30 = arg0;
    native_fn_02008008(temp_r0);
    return temp_r4;
}
