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
extern u32 native_fn_02066c3c();
u32 native_main_0204b948(s32 arg0, u32 arg1, u32 arg2, u32 arg3, u8 arg4) {
    u8 temp_r1;
    u8 temp_r1_2;
    void *temp_r0;

    temp_r0 = (void *) native_fn_02066c3c();
    if (M2C_FIELD(temp_r0, u8 *, 0) != arg0) {
        return 0U;
    }
    temp_r1 = M2C_FIELD(temp_r0, u8 *, 1);
    if ((u32) temp_r1 < arg1) {
        return 0U;
    }
    if ((u32) temp_r1 >= arg3) {
        return 0U;
    }
    temp_r1_2 = M2C_FIELD(temp_r0, u8 *, 2);
    if ((u32) temp_r1_2 < arg2) {
        return 0U;
    }
    if ((u32) temp_r1_2 < (u32) arg4) {
        return 1U;
    }
    return 0U;
}
