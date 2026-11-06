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
extern u32 native_fn_02041510();
extern u32 native_fn_0204bb28();
extern u32 native_fn_0206157c();
extern u32 native_fn_020ba574();
extern u32 native_fn_020cf41c();
extern u8 native_data_021d6b40[];
u32 native_main_020cf3d8(void) {
    if (native_fn_0206157c() != 1) {
        goto block_2;
    }
    native_fn_02041510(1, 2, 0xA);
    native_fn_020cf41c();
    return *(u32 *)native_data_021d6b40;
block_2:
    native_fn_020ba574();
    native_fn_0204bb28();
    return 0x10U;
}
