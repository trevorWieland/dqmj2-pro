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
extern u32 native_fn_0204b4c0();
extern u32 native_fn_0205f98c();
u32 native_main_0204b45c(void *arg0, s32 arg1) {
    s32 temp_r1;
    u32 temp_r0;
    u32 temp_r0_2;

    temp_r0_2 = M2C_FIELD(arg0, u32 *, 0x1C);
    if (temp_r0_2 == 0) {
        return temp_r0_2;
    }
    temp_r0 = native_fn_0205f98c(temp_r0_2, 2);
    M2C_FIELD(arg0, s32 *, 0x30) = arg1;
    if (temp_r0 == 0) {
        return temp_r0;
    }
    temp_r1 = M2C_FIELD(temp_r0, s32 *, 0x7C);
    if (arg1 == 0) {
        M2C_FIELD(temp_r0, s32 *, 0x7C) = (s32) (temp_r1 & ~2);
        return temp_r0;
    }
    M2C_FIELD(temp_r0, s32 *, 0x7C) = (s32) (temp_r1 | 2);
    return native_fn_0204b4c0(arg0, (u8) M2C_FIELD(arg0, s32 *, 0x34));
}
