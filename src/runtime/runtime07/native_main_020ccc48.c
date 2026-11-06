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
extern u32 native_fn_02049130();
extern u32 native_fn_0205f9e4();
extern u32 native_fn_0206b35c();
extern u8 native_data_020e2f38[];
extern u8 native_data_02101ae8[];
extern u8 native_data_021d682c[];
u32 native_main_020ccc48(void *arg0) {
    if (*native_data_020e2f38 != 0) {
        native_fn_02049130(arg0, 6, M2C_FIELD(native_data_021d682c, s32 *, 0xC));
        native_fn_0205f9e4(M2C_FIELD(native_data_021d682c, s32 *, 0xC));
    }
    if (M2C_FIELD(arg0, s8 *, 0x10) == 2) {
        native_fn_0206b35c();
    }
    M2C_FIELD(native_data_02101ae8, s32 *, 0xC84) = 1;
    return (u32) native_data_02101ae8;
}
