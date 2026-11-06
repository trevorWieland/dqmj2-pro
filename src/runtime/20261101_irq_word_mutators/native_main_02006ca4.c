typedef unsigned char u8;
typedef unsigned int u32;
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
typedef struct {
    u8 unknown_0[0x4];
    u32 field_4;
} Record_native_data_020e33c0;
extern Record_native_data_020e33c0 native_data_020e33c0;
u32 native_main_02006ca4(void) {
    u32 temp_r0;
    u32 var_r4;

    temp_r0 = native_fn_02007ff4();
    var_r4 = 0;
    if (native_data_020e33c0.field_4 != 0) {
        var_r4 = native_data_020e33c0.field_4;
        native_data_020e33c0.field_4 = (u32) (native_data_020e33c0.field_4 - 1);
    }
    native_fn_02008008(temp_r0);
    return var_r4;
}
