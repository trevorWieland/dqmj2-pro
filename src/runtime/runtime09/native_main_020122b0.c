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
extern u32 native_fn_020119d0();
u32 native_main_020122b0(void) {
    u16 temp_r0;
    u32 temp_r4;
    void *temp_r1;

    temp_r4 = native_fn_020119c0();
    if (native_fn_020119d0() == 0) {
        goto block_2;
    }
    return 0U;
block_2:
    native_fn_020072d0(M2C_FIELD(temp_r4, void **, 4), 2);
    temp_r1 = M2C_FIELD(temp_r4, void **, 4);
    temp_r0 = M2C_FIELD(temp_r1, u16 *, 0);
    if (temp_r0 == 9) {
        goto block_8;
    }
    if (temp_r0 == 0xA) {
        goto block_6;
    }
    if (temp_r0 == 0xB) {
        goto block_6;
    }
    goto block_7;
block_6:
    goto block_10;
block_7:
    goto block_11;
block_8:
    native_fn_020072d0(temp_r1 + 0x182, 2);
    if (M2C_FIELD(M2C_FIELD(temp_r4, void **, 4), u16 *, 0x182) != 0) {
        goto block_10;
    }
    return 0U;
block_10:
    native_fn_020072d0(M2C_FIELD(temp_r4, void **, 4) + 0xBC, 2);
    return (u32) M2C_FIELD(M2C_FIELD(temp_r4, void **, 4), u16 *, 0xBC);
block_11:
    return 0U;
}
