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
extern u32 native_fn_020096f8();
extern u32 native_fn_02009780();
void native_main_02009470(s32 arg0, s32 arg1, s32 arg2, s32 arg3, s32 arg4) {
    u32 temp_r0;

    temp_r0 = native_fn_020096f8(1);
    if (temp_r0 == 0) {
        return;
    }
    M2C_FIELD(temp_r0, s32 *, 4) = arg0;
    M2C_FIELD(temp_r0, s32 *, 8) = arg1;
    M2C_FIELD(temp_r0, s32 *, 0xC) = arg2;
    M2C_FIELD(temp_r0, s32 *, 0x10) = arg3;
    M2C_FIELD(temp_r0, s32 *, 0x14) = arg4;
    native_fn_02009780();
}
