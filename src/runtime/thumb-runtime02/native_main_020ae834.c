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
extern u8 native_data_020e0dc8[];
extern u8 native_data_020e0de0[];
extern u8 native_data_020e0dec[];
extern u8 native_data_020e0df4[];
u32 native_main_020ae834(void **arg0, u32 arg1) {
    void *temp_r4;

    temp_r4 = *arg0;
    if ((s32) M2C_FIELD(temp_r4, s32 *, 0x5E8) > 0) {
        native_fn_020ac6f4(arg0, arg1, native_data_020e0dc8);
        native_fn_020ac710(arg0, arg1, M2C_FIELD(temp_r4, s32 *, 0x198));
        native_fn_020ac6f4(arg0, arg1, M2C_FIELD(temp_r4, u8 **, 0x5E0));
        native_fn_020ac6f4(arg0, arg1, native_data_020e0de0);
        native_fn_020ac710(arg0, arg1, M2C_FIELD(temp_r4, s32 *, 0x1A4));
        native_fn_020ac6f4(arg0, arg1, native_data_020e0dec);
        M2C_FIELD(temp_r4, s32 *, 0x5E8) = 0;
    }
    if ((s32) M2C_FIELD(temp_r4, s32 *, 0x5F8) > 0) {
        native_fn_020ac6f4(arg0, arg1, native_data_020e0df4);
        native_fn_020ac710(arg0, arg1, M2C_FIELD(temp_r4, s32 *, 0x198));
        native_fn_020ac6f4(arg0, arg1, M2C_FIELD(temp_r4, u8 **, 0x5F0));
        native_fn_020ac6f4(arg0, arg1, native_data_020e0dec);
        M2C_FIELD(temp_r4, s32 *, 0x5F8) = 0;
    }
    return 0U;
}
