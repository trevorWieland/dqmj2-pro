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
extern u32 native_fn_02049130();
extern u32 native_fn_0204b5b0();
extern u32 native_fn_0204b61c();
extern u32 native_fn_0205f9e4();
extern u32 native_fn_0206b35c();
extern u32 native_fn_020c59bc();
extern u32 native_fn_020c8fa8();
extern u32 native_fn_020c9294();
extern u8 native_data_020e2e88[];
extern u8 native_data_02101ae8[];
extern u8 native_data_021d64b8[];
u32 native_main_020c9308(u32 arg0) {
    if (M2C_FIELD((void *) native_fn_020c8fa8(), s8 *, 0x10) == 0) {
        goto block_2;
    }
    if (M2C_FIELD((void *) native_fn_020c8fa8(), s8 *, 0x10) != 5) {
        goto block_3;
    }
block_2:
    native_fn_02049130(native_fn_020c8fa8(), 0xD, M2C_FIELD(native_data_021d64b8, s32 *, 4));
    native_fn_0205f9e4(M2C_FIELD(native_data_021d64b8, s32 *, 4));
    goto block_6;
block_3:
    if (M2C_FIELD((void *) native_fn_020c8fa8(), s8 *, 0x10) != 3) {
        goto block_5;
    }
    native_fn_02049130(native_fn_020c8fa8(), 0xD, M2C_FIELD(native_data_021d64b8, s32 *, 4));
    native_fn_0204b5b0(M2C_FIELD(native_data_021d64b8, s32 *, 4), 0xB8);
    native_fn_0205f9e4(M2C_FIELD(native_data_021d64b8, s32 *, 4));
    goto block_6;
block_5:
    native_fn_0204b61c(M2C_FIELD(native_data_021d64b8, s32 *, 4), 0);
block_6:
    if (*native_data_020e2e88 != 0) {
        goto block_8;
    }
    native_fn_0204b61c(M2C_FIELD(native_data_021d64b8, s32 *, 4), 0);
block_8:
    native_fn_020c9294(arg0);
    if (M2C_FIELD((void *) native_fn_020c8fa8(), s8 *, 0x10) != 1) {
        goto block_10;
    }
    native_fn_0206b35c();
block_10:
    if (M2C_FIELD((void *) native_fn_020c8fa8(), s8 *, 0x10) != 2) {
        goto block_12;
    }
    native_fn_020c59bc();
block_12:
    M2C_FIELD(native_data_02101ae8, s32 *, 0xC84) = 1;
    return (u32) native_data_02101ae8;
}
