typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define NULL ((void *)0)
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
typedef struct {
    u8 unknown_0[0x4];
    u32 field_4;
    s32 field_8;
    u8 unknown_c[0x14];
    u32 field_20;
} Record_native_data_020e3780;
extern Record_native_data_020e3780 native_data_020e3780;
u32 native_main_020099e0(void) {
    u32 temp_r0;
    u32 var_r4;

    temp_r0 = native_fn_02007ff4();
    if (native_data_020e3780.field_8 == 0) {
        var_r4 = native_data_020e3780.field_4;
    } else {
        var_r4 = native_data_020e3780.field_20;
    }
    native_fn_02008008(temp_r0);
    return var_r4;
}
