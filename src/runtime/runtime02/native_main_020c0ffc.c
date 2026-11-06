typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_fn_0205e7a8();
extern u32 native_fn_02062a10();
extern u32 native_fn_02066c3c();
extern u32 native_fn_02068bf4();
extern u32 native_fn_02069330();
extern u32 native_fn_0206be08();
extern u32 native_fn_0206be14();
extern u32 native_fn_0206c18c();
extern u32 native_fn_020bf7e0();
extern u32 native_fn_020c0200();
extern u32 native_fn_020c0210();
extern u32 native_fn_020c0f54();
extern u8 native_data_020e2cf0[];
extern u8 native_data_021d4bec[];
u32 native_main_020c0ffc(void *arg0, s8 arg1) {
    u32 temp_r0_2;
    u32 temp_r0_3;
    u32 temp_r4;
    u32 var_r4;
    void *temp_r0;

    var_r4 = 0;
    temp_r0 = (void *) native_fn_02066c3c();
    temp_r0_2 = native_fn_020c0f54(M2C_FIELD(temp_r0, u8 *, 1), M2C_FIELD(temp_r0, u8 *, 2));
    if (temp_r0_2 != -1U) {
        temp_r0_3 = native_fn_020bf7e0((M2C_FIELD(native_data_021d4bec, u8 *, 4) * 6) + temp_r0_2);
        if (temp_r0_3 != 0) {
            native_fn_020c0210();
            temp_r4 = native_fn_02062a10(temp_r0_3);
            native_fn_02069330(temp_r4, 0, 0, 0, 0, (s32) *native_data_020e2cf0, 0xF, native_fn_0206c18c(1));
            M2C_FIELD(arg0, s8 *, 2) = arg1;
            M2C_FIELD(arg0, u8 *, 0) = (u8) M2C_FIELD(temp_r0, u8 *, 1);
            M2C_FIELD(arg0, u8 *, 1) = (u8) M2C_FIELD(temp_r0, u8 *, 2);
            M2C_FIELD(native_data_021d4bec, u32 *, 0x10) = temp_r0_3;
            native_fn_020c0200();
            if (native_fn_02068bf4() != 0) {
                native_fn_0206be08(0, 0);
                native_fn_0206be14(1);
            } else {
                native_fn_0206be08(0, 1);
                native_fn_0206be08(1, 1);
            }
            native_fn_0205e7a8(-1, 0x52);
            var_r4 = 1;
        }
    }
    return var_r4;
}
