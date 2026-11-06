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
extern u32 native_fn_0205e844();
extern u32 native_fn_02081cdc();
extern u32 native_fn_02081e80();
extern u8 native_data_021c6e78[] __attribute__((aligned(2)));
u32 native_main_02081fc8(u32 arg0, s32 arg1) {
    s8 var_r1;
    u32 var_r4;

    var_r4 = 0;
    if (arg1 == 0) {
        goto block_6;
    }
    if (M2C_FIELD(native_data_021c6e78, s32 *, 4) != 0) {
        goto block_3;
    }
    native_fn_0205e844(0x40);
    M2C_FIELD(native_data_021c6e78, s32 *, 4) = 0xA;
    goto block_6;
block_3:
    if (M2C_FIELD(native_data_021c6e78, s32 *, 4) != 0xA) {
        goto block_6;
    }
    if (native_fn_0205e844(0x40) == 0) {
        goto block_6;
    }
    M2C_FIELD(native_data_021c6e78, s32 *, 4) = 0x64;
block_6:
    if (M2C_FIELD(native_data_021c6e78, s8 *, 1) != 0) {
        goto block_8;
    }
    native_fn_02081cdc(arg0);
    M2C_FIELD(native_data_021c6e78, s8 *, 1) = 0xA;
    goto block_19;
block_8:
    if (M2C_FIELD(native_data_021c6e78, s8 *, 1) != 0xA) {
        goto block_14;
    }
    if (native_fn_02081e80() == 0) {
        goto block_19;
    }
    if (arg1 == 0) {
        goto block_12;
    }
    var_r1 = 0x14;
    goto block_13;
block_12:
    var_r1 = 0x64;
block_13:
    M2C_FIELD(native_data_021c6e78, s8 *, 1) = var_r1;
    goto block_19;
block_14:
    if (M2C_FIELD(native_data_021c6e78, s8 *, 1) != 0x14) {
        goto block_18;
    }
    if (M2C_FIELD(native_data_021c6e78, s32 *, 4) != 0x64) {
        goto block_17;
    }
    M2C_FIELD(native_data_021c6e78, s8 *, 1) = 0x64;
block_17:
    goto block_19;
block_18:
    M2C_FIELD(native_data_021c6e78, s32 *, 4) = 0;
    var_r4 = 1;
block_19:
    return var_r4;
}
