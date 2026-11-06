typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define NULL ((void *)0)
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u8 native_data_020e5d80[];
u32 native_main_02011eb4(void) {
    u32 temp_r0;
    u16 var_r4;

    temp_r0 = native_fn_02007ff4();
    if (M2C_FIELD(native_data_020e5d80, void **, 4) != NULL) {
        var_r4 = M2C_FIELD(M2C_FIELD(native_data_020e5d80, void **, 4), u16 *, 0x150);
    } else {
        var_r4 = 0;
    }
    native_fn_02008008(temp_r0);
    return (u32) var_r4;
}
