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
extern u32 native_fn_020ac6f4();
extern u32 native_fn_020ac710();
extern u8 native_data_020e05ec[];
extern u8 native_data_020e05f8[];
extern u8 native_data_020e0604[];
extern u8 native_data_020e0614[];
extern u8 native_data_020e061c[];
u32 native_main_020aaf08(void **arg0, void *arg1) {
    void *temp_r4;

    temp_r4 = *arg0;
    native_fn_020ac6f4(arg0, temp_r4 + 0x210, native_data_020e05ec);
    native_fn_020ac6f4(arg0, temp_r4 + 0x210, native_data_020e05f8);
    native_fn_020ac710(arg0, temp_r4 + 0x210, M2C_FIELD(temp_r4, s32 *, 0x198));
    native_fn_020ac6f4(arg0, temp_r4 + 0x210, native_data_020e0604);
    native_fn_020ac710(arg0, temp_r4 + 0x210, M2C_FIELD(arg1, s32 *, 0));
    native_fn_020ac6f4(arg0, temp_r4 + 0x210, native_data_020e0614);
    native_fn_020ac6f4(arg0, temp_r4 + 0x210, M2C_FIELD(arg1, u8 **, 0x14));
    native_fn_020ac6f4(arg0, temp_r4 + 0x210, native_data_020e061c);
    return 0U;
}
