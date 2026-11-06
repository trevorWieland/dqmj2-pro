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
extern u32 native_fn_0204b61c();
extern u8 native_data_020e2e88[];
extern u8 native_data_02101ae8[];
extern u8 native_data_021d64b8[];
u32 native_main_020c957c(u8 arg0) {
    *native_data_020e2e88 = arg0;
    if (arg0 == 0) {
        native_fn_0204b61c(M2C_FIELD(native_data_021d64b8, s32 *, 4), 0);
    }
    M2C_FIELD(native_data_02101ae8, s32 *, 0xC84) = 1;
    return (u32) native_data_02101ae8;
}
