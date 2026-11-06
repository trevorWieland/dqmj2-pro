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
extern u32 native_fn_020449d4();
extern u32 native_fn_02062a10();
u32 native_main_0207cbec(s32 *arg0, s32 *arg1) {
    u8 temp_r0;
    s32 temp_r4_2;
    u32 temp_r4;
    u8 temp_r5;
    s32 temp_r6;

    temp_r4_2 = *arg1;
    temp_r6 = *arg0;
    if (temp_r4_2 == 0) {
        return -1U;
    }
    if (temp_r6 == 0) {
        return 1U;
    }
    temp_r5 = M2C_FIELD((void *) native_fn_02062a10(temp_r6), u8 *, 0x30);
    temp_r0 = M2C_FIELD((void *) native_fn_02062a10(temp_r4_2), u8 *, 0x30);
    if (temp_r5 != temp_r0) {
        return temp_r0 - temp_r5;
    }
    temp_r4 = native_fn_020449d4(M2C_FIELD((void *) native_fn_02062a10(temp_r4_2), s16 *, 0x18));
    return ((u32) (M2C_FIELD(temp_r4, u16 *, 6) << 0x13) >> 0x13) - ((u32) (M2C_FIELD((void *) native_fn_020449d4(M2C_FIELD((void *) native_fn_02062a10(temp_r6), s16 *, 0x18)), u16 *, 6) << 0x13) >> 0x13);
}
