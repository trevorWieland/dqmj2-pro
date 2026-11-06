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
extern u32 native_fn_02034758();
extern u8 native_data_020d9160[];
u32 native_main_020368f8(void *arg0, u32 arg1) {
    u32 temp_r0;

    native_fn_02034758(arg1, arg0);
    temp_r0 = *(u32 *)(native_data_020d9160 + (M2C_FIELD(M2C_FIELD(arg0, void **, 0), u8 *, 7) * 4));
    M2C_FIELD(arg0, u32 *, 4) = temp_r0;
    return temp_r0;
}
