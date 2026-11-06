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
extern u32 native_fn_020273d8();
extern u32 native_fn_020273f0();
extern u32 native_fn_020404f0();
extern u32 native_fn_020406a8();
extern u32 native_fn_020406c8();
extern u32 native_fn_020612ec();
extern u32 native_fn_0206157c();
extern u32 native_fn_02061950();
extern u32 native_fn_02062328();
extern u32 native_fn_0206dcd0();
extern u32 native_fn_0206dec8();
extern u32 native_fn_020c4104();
extern u8 native_data_021c36fc[] __attribute__((aligned(2)));
u32 native_main_020675e8(void) {
    u32 temp_r0;
    u32 var_r4;

    var_r4 = 0;
    if (M2C_FIELD(native_data_021c36fc, s32 *, 8) != 0xFFFF) {
        goto block_2;
    }
    return 1U;
block_2:
    if (M2C_FIELD(native_data_021c36fc, s32 *, 8) != 0) {
        goto block_11;
    }
    if (native_fn_020273f0() != 0) {
        goto block_22;
    }
    M2C_FIELD(native_data_021c36fc, s32 *, 8) = 0xA;
    native_fn_020273d8(3);
    native_fn_020406a8(1);
    native_fn_020404f0(0x25);
    temp_r0 = native_fn_020c4104();
    if (temp_r0 == 1) {
        goto block_7;
    }
    if (temp_r0 == 2) {
        goto block_8;
    }
    goto block_9;
block_7:
    native_fn_020612ec(0xA, 0, 0x6000, 0);
    goto block_10;
block_8:
    native_fn_020612ec(9, 0, 0x6000, 0);
    goto block_10;
block_9:
    native_fn_020612ec(0x10, 0, 0x6000, 0);
block_10:
    native_fn_0206dcd0(0);
    native_fn_020406c8(0);
    native_fn_02061950(0x10);
    goto block_22;
block_11:
    if (M2C_FIELD(native_data_021c36fc, s32 *, 8) == 5) {
        goto block_22;
    }
    if (M2C_FIELD(native_data_021c36fc, s32 *, 8) != 0xA) {
        goto block_15;
    }
    native_fn_0206157c();
    if (native_fn_020273f0() != 0) {
        goto block_22;
    }
    M2C_FIELD(native_data_021c36fc, s32 *, 8) = 0x14;
    native_fn_02062328();
    native_fn_020406a8(0);
    goto block_22;
block_15:
    if (M2C_FIELD(native_data_021c36fc, s32 *, 8) != 0x14) {
        goto block_17;
    }
    M2C_FIELD(native_data_021c36fc, s32 *, 8) = 0x1E;
    native_fn_0206dec8();
    goto block_22;
block_17:
    if (M2C_FIELD(native_data_021c36fc, s32 *, 8) != 0x1E) {
        goto block_20;
    }
    if (native_fn_0206157c() == 0) {
        goto block_22;
    }
    M2C_FIELD(native_data_021c36fc, s32 *, 8) = 0x28;
    goto block_22;
block_20:
    if (M2C_FIELD(native_data_021c36fc, s32 *, 8) != 0x28) {
        goto block_22;
    }
    var_r4 = 1;
block_22:
    return var_r4;
}
