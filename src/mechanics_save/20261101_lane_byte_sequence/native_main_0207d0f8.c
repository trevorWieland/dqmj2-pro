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

extern u32 native_fn_0207afec(s32);

u32 native_main_0207d0f8(u32 arg0, u32 arg1, s32 arg2) {

    s32 var_r0;

    u8 temp_r0;

    u8 temp_r4;



    temp_r4 = M2C_FIELD((void *) native_fn_0207afec(arg0), u8 *, 0x1F);

    temp_r0 = M2C_FIELD((void *) native_fn_0207afec(arg0), u8 *, 0x20);

    if (temp_r4 == arg2) {

        goto block_3;

    }

    if (temp_r0 == arg2) {

        goto block_3;

    }

    goto block_6;

block_3:

    var_r0 = (s32) (arg1 + (arg1 >> 0x1F)) >> 1;

    if (var_r0 >= 1) {

        goto block_5;

    }

    var_r0 = 1;

block_5:

    return (u32) var_r0;

block_6:

    return arg1;

}

