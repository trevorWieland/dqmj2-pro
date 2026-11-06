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
extern u32 native_fn_02086948();
extern u32 native_fn_02086a98();
extern u32 native_fn_02086b14();
extern u32 native_fn_02086b68();
extern u32 native_fn_02087e44();
u32 native_main_020861e4(void *arg0) {
    s32 temp_r1;

    if (M2C_FIELD(arg0, s32 *, 0x64) != 0) {
        goto block_6;
    }
    temp_r1 = M2C_FIELD(arg0, s32 *, 0);
    if (temp_r1 == 4) {
        goto block_4;
    }
    if (temp_r1 == 7) {
        goto block_4;
    }
    goto block_5;
block_4:
    native_fn_02086948(arg0, 0);
    goto block_7;
block_5:
    native_fn_02086948(arg0, 1);
    goto block_7;
block_6:
    native_fn_02086a98();
block_7:
    native_fn_02087e44(M2C_FIELD(arg0, s32 *, 0x44), 0);
    native_fn_02086b68(arg0, M2C_FIELD(arg0, s32 *, 0x64), M2C_FIELD(arg0, u16 *, 0x6C));
    native_fn_02086b14(arg0, 0);
    return 1U;
}
