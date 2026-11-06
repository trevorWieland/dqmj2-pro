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
extern void native_fn_0203a078(u32 *);
extern void native_fn_0203a554(u32);
extern u8 native_data_020f552c[];
u32 native_main_0203a1d4(u32 *arg0, u32 arg1, s32 arg2) {
    u32 temp_r4;

    if (*arg0 == 0) {
        goto block_2;
    }
    native_fn_0203a078(arg0);
block_2:
    temp_r4 = (arg1 * 0x174) + (u32) native_data_020f552c;
    if (M2C_FIELD(temp_r4, s32 *, 0x12C) != 0) {
        goto block_4;
    }
    return 0U;
block_4:
    if (((s32) (M2C_FIELD(temp_r4, u32 *, 0x110) << 0x1F) >> 0x1F) == 0) {
        goto block_8;
    }
    if (arg2 >= (s32) M2C_FIELD(temp_r4, s32 *, 0x150)) {
        goto block_7;
    }
    return 0U;
block_7:
    native_fn_0203a554(temp_r4);
block_8:
    M2C_FIELD(temp_r4, s32 *, 0x150) = arg2;
    M2C_FIELD(temp_r4, s32 *, 0x110) = (s32) ((M2C_FIELD(temp_r4, s32 *, 0x110) & ~1) | 1);
    M2C_FIELD(temp_r4, u32 **, 0x14C) = arg0;
    *arg0 = temp_r4;
    return temp_r4;
}
