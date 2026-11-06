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
extern u32 native_fn_020642dc();
extern u32 native_fn_020c3a00();
extern u32 native_fn_020cc74c();
void native_main_020cc7d8(void) {
    s32 temp_r0;

    if (native_fn_020c3a00() != 3) {
        goto block_2;
    }
    native_fn_020cc74c(6);
    return;
block_2:
    if (native_fn_020c3a00() != 4) {
        goto block_4;
    }
    native_fn_020cc74c(5);
    return;
block_4:
    temp_r0 = (s32) native_fn_020642dc();
    if (temp_r0 > 0x16) {
        goto block_15;
    }
    if (temp_r0 >= 0x16) {
        goto block_27;
    }
    if (temp_r0 <= 0xB) {
        goto block_8;
    }
    return;
block_8:
    if (temp_r0 >= 0xA) {
        goto block_10;
    }
    return;
block_10:
    if (temp_r0 == 0xA) {
        goto block_13;
    }
    if (temp_r0 == 0xB) {
        goto block_13;
    }
    goto block_14;
block_13:
    goto block_26;
block_14:
    return;
block_15:
    if (temp_r0 > 0x1D) {
        goto block_24;
    }
    if (temp_r0 >= 0x17) {
        goto block_18;
    }
    return;
block_18:
    if (temp_r0 == 0x17) {
        goto block_21;
    }
    if (temp_r0 == 0x18) {
        goto block_21;
    }
    goto block_22;
block_21:
    goto block_27;
block_22:
    if (temp_r0 == 0x1D) {
        goto block_28;
    }
    return;
block_24:
    if (temp_r0 == 0x2B) {
        goto block_29;
    }
    return;
block_26:
    native_fn_020cc74c(3);
    return;
block_27:
    native_fn_020cc74c(1);
    return;
block_28:
    native_fn_020cc74c(2);
    return;
block_29:
    native_fn_020cc74c(4);
    return;
}
