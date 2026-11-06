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
extern u32 native_fn_020824b4();
extern u32 native_fn_020824c4();
extern u32 native_fn_020830e4();
extern u8 native_data_021c72a0[];
void native_main_02083000(void *arg0) {
    u16 temp_r0;
    u16 temp_r0_2;

    if (M2C_FIELD(arg0, u16 *, 2) == 0) {
        goto block_8;
    }
    native_fn_020824c4();
    temp_r0 = M2C_FIELD(arg0, u16 *, 2);
    if (temp_r0 != 0xC) {
        goto block_3;
    }
    native_fn_020824b4(9);
    return;
block_3:
    if (temp_r0 != 0xB) {
        goto block_5;
    }
    native_fn_020824b4(9);
    return;
block_5:
    if (temp_r0 != 1) {
        goto block_7;
    }
    native_fn_020824b4(8);
    return;
block_7:
    native_fn_020824b4(9);
    return;
block_8:
    temp_r0_2 = M2C_FIELD(arg0, u16 *, 8);
    if (temp_r0_2 != 8) {
        goto block_10;
    }
    return;
block_10:
    if (temp_r0_2 != 7) {
        goto block_14;
    }
    native_fn_020824b4(4);
    if (native_fn_020830e4() != 0) {
        goto block_13;
    }
    native_fn_020824b4(3);
    return;
block_13:
    M2C_FIELD(native_data_021c72a0, u16 *, 0xC) = (u16) M2C_FIELD(arg0, u16 *, 0xA);
    return;
block_14:
    if (temp_r0_2 != 6) {
        goto block_16;
    }
    return;
block_16:
    if (temp_r0_2 != 9) {
        goto block_18;
    }
    native_fn_020824c4(0x14);
    native_fn_020824b4(9);
    return;
block_18:
    if (temp_r0_2 != 0x1A) {
        goto block_20;
    }
    return;
block_20:
    native_fn_020824b4(9);
    return;
}
