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
extern u32 native_fn_0202a634();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_020808cc();
extern u32 native_fn_02080ba8();
extern u32 native_fn_02081168();
u32 native_main_020804f4(u32 arg0) {
    u16 temp_r0;
    u32 temp_r4;
    u32 var_r5;

    var_r5 = 0;
    temp_r4 = native_fn_0202a634();
    native_fn_020808cc();
    temp_r0 = M2C_FIELD(temp_r4, u16 *, 2);
    if (!(temp_r0 & 2)) {
        goto block_2;
    }
    var_r5 = 8;
    goto block_6;
block_2:
    if (!(temp_r0 & 8)) {
        goto block_4;
    }
    native_fn_02081168(0);
    native_fn_0205e7a8(-1, 0x52);
    goto block_6;
block_4:
    if (!(temp_r0 & 1)) {
        goto block_6;
    }
    var_r5 = native_fn_02080ba8(arg0);
block_6:
    return var_r5;
}
