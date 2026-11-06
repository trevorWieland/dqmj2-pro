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
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
extern u32 native_fn_02008e0c();
extern u32 native_fn_0202a1e0();
extern u32 native_fn_02049940();
extern u32 native_fn_0207ea7c();
extern u32 native_fn_0207eebc();
extern u32 native_fn_0207f3a0();
extern u32 native_fn_02080340();
extern u32 native_fn_020811b0();
extern u32 native_fn_02081830();
extern u32 native_fn_02081894();
extern u8 native_data_021c6c14[];
extern u8 native_data_021c6c38[];
extern u8 native_data_021c6c5c[];
u32 native_main_0207e7e4(u32 arg0) {
    u32 temp_r4;

    native_fn_02008e0c(arg0, native_data_021c6c38, 0x10);
    native_fn_0207f3a0(1);
    M2C_FIELD(native_data_021c6c14, s32 *, 0x10) = 0;
    M2C_FIELD(native_data_021c6c14, s32 *, 4) = 1;
    M2C_FIELD(native_data_021c6c14, s32 *, 8) = 0;
    M2C_FIELD(native_data_021c6c14, u8 **, 0x14) = native_data_021c6c5c;
    M2C_FIELD(native_data_021c6c14, s8 *, 1) = 1;
    temp_r4 = native_fn_0202a1e0(2U);
    native_fn_02049940(1);
    native_fn_02081830();
    native_fn_02080340();
    native_fn_0207ea7c();
    native_fn_020811b0(0, 0);
    native_fn_0207eebc();
    native_fn_02081894();
    return native_fn_0202a1e0(temp_r4);
}
