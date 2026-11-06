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
extern u32 native_fn_02047ff0();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_020627a0();
extern u32 native_fn_02062a10();
extern u32 native_fn_020c42c8();
extern u32 native_fn_020c4318();
extern u32 native_fn_020c484c();
extern u32 native_fn_020c48bc();
extern u32 native_fn_020c48d0();
extern u32 native_fn_020c48e8();
extern u32 native_fn_020c4908();
extern u32 native_fn_020c4918();
extern u32 native_fn_020c59bc();
extern u32 native_fn_020c59cc();
extern u32 native_fn_020c5a7c();
extern u8 native_data_021d6384[];
u32 native_main_020c7cc4(void) {
    u32 var_r4;

    var_r4 = 0;
    if ((s8) M2C_FIELD(native_data_021d6384, u8 *, 0) != 0) {
        goto block_2;
    }
    native_fn_020c48bc();
    native_fn_020c48d0(5, 6, 0x3A);
    native_fn_020c48e8(0x57);
    native_fn_020c484c(0);
    native_fn_020c4908(1);
    native_fn_020c59cc(0);
    native_fn_02047ff0(native_fn_02062a10(M2C_FIELD(native_data_021d6384, s32 *, 0x24)), 0x14, 0);
    M2C_FIELD(native_data_021d6384, u8 *, 0) = 0xA;
    goto block_21;
block_2:
    if ((s8) M2C_FIELD(native_data_021d6384, u8 *, 0) != 0xA) {
        goto block_8;
    }
    if (native_fn_020c4318() == 0) {
        goto block_21;
    }
    if (native_fn_020c4918() == 0) {
        goto block_6;
    }
    native_fn_0205e7a8(-1, 0x52);
    M2C_FIELD(native_data_021d6384, u8 *, 0) = 0x14;
    goto block_7;
block_6:
    native_fn_0205e7a8(-1, 0x53);
    M2C_FIELD(native_data_021d6384, u8 *, 0) = 0;
    native_fn_020c59cc(1);
    var_r4 = 1;
block_7:
    native_fn_020c42c8();
    goto block_21;
block_8:
    if ((s8) M2C_FIELD(native_data_021d6384, u8 *, 0) != 0x14) {
        goto block_10;
    }
    native_fn_020c48bc();
    native_fn_020c48d0(0xF, 4, 0x3F);
    native_fn_020c48e8(-1);
    native_fn_020c484c(0);
    native_fn_020c4908(1);
    native_fn_020c59cc(0);
    M2C_FIELD(native_data_021d6384, u8 *, 0) = 0x1E;
    goto block_21;
block_10:
    if ((s8) M2C_FIELD(native_data_021d6384, u8 *, 0) != 0x1E) {
        goto block_16;
    }
    if (native_fn_020c4318() == 0) {
        goto block_21;
    }
    if (native_fn_020c4918() == 0) {
        goto block_14;
    }
    native_fn_0205e7a8(-1, 0x52);
    M2C_FIELD(native_data_021d6384, u8 *, 0) = 0x28;
    goto block_15;
block_14:
    native_fn_0205e7a8(-1, 0x53);
    M2C_FIELD(native_data_021d6384, u8 *, 0) = 0;
    native_fn_020c59cc(1);
    var_r4 = 1;
block_15:
    native_fn_020c42c8();
    goto block_21;
block_16:
    if ((s8) M2C_FIELD(native_data_021d6384, u8 *, 0) != 0x28) {
        goto block_18;
    }
    native_fn_020c48bc();
    native_fn_020c48d0(9, 1, 0x13);
    native_fn_020c48e8(-1);
    native_fn_020c59cc(0);
    M2C_FIELD(native_data_021d6384, u8 *, 0) = 0x32;
    goto block_21;
block_18:
    if ((s8) M2C_FIELD(native_data_021d6384, u8 *, 0) != 0x32) {
        goto block_21;
    }
    if (native_fn_020c4318() == 0) {
        goto block_21;
    }
    native_fn_020627a0(M2C_FIELD(native_data_021d6384, s32 *, 0x24));
    native_fn_020c5a7c(M2C_FIELD(native_data_021d6384, s32 *, 0x20));
    M2C_FIELD(native_data_021d6384, u8 *, 0) = 0;
    native_fn_020c59cc(1);
    var_r4 = 1;
    native_fn_0205e7a8(-1, 0x52);
block_21:
    native_fn_020c59bc();
    return var_r4;
}
