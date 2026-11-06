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
extern u32 native_fn_02011834();
extern u32 native_fn_020118a4();
extern u32 native_fn_020119c0();
extern u32 native_fn_02011a34();
u32 native_main_02012d84(u32 arg0, u32 arg1) {
    u16 temp_r0_2;
    u32 temp_r0;
    u32 temp_r6;
    u32 var_r0;
    void *temp_r1;

    temp_r6 = native_fn_020119c0();
    temp_r0 = native_fn_02011a34(5, 7, 9, 8, 0xA, 0xB);
    if (temp_r0 == 0) {
        goto block_2;
    }
    return temp_r0;
block_2:
    temp_r1 = M2C_FIELD(temp_r6, void **, 4);
    temp_r0_2 = M2C_FIELD(temp_r1, u16 *, 0);
    if (temp_r0_2 == 7) {
        goto block_5;
    }
    if (temp_r0_2 == 9) {
        goto block_5;
    }
    goto block_10;
block_5:
    if (arg1 < 1U) {
        goto block_7;
    }
    if (arg1 <= 0xFU) {
        goto block_8;
    }
block_7:
    return 6U;
block_8:
    native_fn_020072d0(temp_r1 + 0x182, 2);
    if (M2C_FIELD(M2C_FIELD(temp_r6, void **, 4), u16 *, 0x182) & (1 << arg1)) {
        goto block_12;
    }
    return 7U;
block_10:
    if (arg1 == 0) {
        goto block_12;
    }
    return 6U;
block_12:
    native_fn_02011834(0xD, arg0);
    var_r0 = native_fn_020118a4(0xD, 1, 1 << arg1);
    if (var_r0 != 0) {
        goto block_14;
    }
    var_r0 = 2;
block_14:
    return var_r0;
}
