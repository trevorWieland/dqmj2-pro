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

u32 native_main_0207cff4(s32 arg0) {

    if (((u32) (M2C_FIELD((void *) native_fn_0207afec(arg0), u16 *, 8) << 0x14) >> 0x1C) != 2) {

        goto block_2;

    }

    if (M2C_FIELD((void *) native_fn_0207afec(arg0), u8 *, 0x1E) == 1) {

        goto block_12;

    }

block_2:

    if (((u32) (M2C_FIELD((void *) native_fn_0207afec(arg0), u16 *, 8) << 0x14) >> 0x1C) == 3) {

        goto block_12;

    }

    if (((u32) (M2C_FIELD((void *) native_fn_0207afec(arg0), u16 *, 8) << 0x14) >> 0x1C) == 8) {

        goto block_7;

    }

    if (arg0 == 0x38) {

        goto block_7;

    }

    if (arg0 == 0xA3) {

        goto block_7;

    }

    goto block_8;

block_7:

    goto block_12;

block_8:

    if (M2C_FIELD((void *) native_fn_0207afec(arg0), u8 *, 0x21) == 0x23) {

        goto block_12;

    }

    if (M2C_FIELD((void *) native_fn_0207afec(arg0), u8 *, 0x21) == 0x24) {

        goto block_12;

    }

    if (M2C_FIELD((void *) native_fn_0207afec(arg0), u8 *, 0x21) == 0x27) {

        goto block_12;

    }

    if (M2C_FIELD((void *) native_fn_0207afec(arg0), u8 *, 0x21) != 0x1E) {

        goto block_13;

    }

block_12:

    return 1U;

block_13:

    return 0U;

}

