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
extern u32 native_fn_020072d0();
extern u32 native_fn_020119c0();
extern u32 native_fn_02011a34();
u32 native_main_020120e8(void) {
    s32 var_r5;
    u16 temp_r5;
    u32 temp_r4;
    void *temp_r0;
    void *temp_r1;
    void *temp_r1_2;

    temp_r4 = native_fn_020119c0();
    if (native_fn_02011a34(2, 7, 8) != 0) {
        return 0U;
    }
    native_fn_020072d0(M2C_FIELD(temp_r4, void **, 4) + 0xC, 4);
    temp_r1 = M2C_FIELD(temp_r4, void **, 4);
    if (M2C_FIELD(temp_r1, s32 *, 0xC) == 1) {
        return 0U;
    }
    native_fn_020072d0(temp_r1 + 0x188, 2);
    temp_r1_2 = M2C_FIELD(temp_r4, void **, 4);
    if (M2C_FIELD(temp_r1_2, u16 *, 0x188) == 0) {
        var_r5 = 1;
    } else {
        var_r5 = 0;
    }
    native_fn_020072d0(temp_r1_2 + 0x3E, 2);
    temp_r0 = M2C_FIELD(temp_r4, void **, 4);
    temp_r5 = M2C_FIELD(temp_r0, u16 *, 0x3E);
    if (var_r5 != 1) {
        return ((temp_r5 + 0x51) & ~0x1F) * 2;
    }
    native_fn_020072d0(temp_r0 + 0xF8, 2);
    return ((((temp_r5 + 0xC) * M2C_FIELD(M2C_FIELD(temp_r4, void **, 4), u16 *, 0xF8)) + 0x29) & ~0x1F) * 2;
}
