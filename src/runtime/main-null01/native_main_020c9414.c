#define NULL ((void *)0)
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
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_0204b61c();
extern u32 native_fn_0206b35c();
extern u32 native_fn_020c59bc();
extern u8 native_data_020e2e88[];
extern u8 native_data_02101ae8[];
extern u8 native_data_021d64b8[];
u32 native_main_020c9414(s32 arg0) {
    s32 temp_r0;

    if (M2C_FIELD(native_data_021d64b8, s32 *, 4) != 0) {
        if (arg0 & 1) {
            native_fn_0204b61c(M2C_FIELD(native_data_021d64b8, s32 *, 4), *native_data_020e2e88);
        } else {
            native_fn_0204b61c(M2C_FIELD(native_data_021d64b8, s32 *, 4), 0U);
        }
    }
    if (M2C_FIELD(native_data_021d64b8, void **, 0x10) != NULL) {
        temp_r0 = M2C_FIELD(M2C_FIELD(native_data_021d64b8, void **, 0x10), s32 *, 0x7C);
        if (arg0 & 8) {
            M2C_FIELD(M2C_FIELD(native_data_021d64b8, void **, 0x10), s32 *, 0x7C) = (s32) (temp_r0 | 2);
        } else {
            M2C_FIELD(M2C_FIELD(native_data_021d64b8, void **, 0x10), s32 *, 0x7C) = (s32) (temp_r0 & ~2);
        }
    }
    if (arg0 & 2) {
        native_fn_0206b35c();
    }
    if (arg0 & 4) {
        native_fn_020c59bc();
    }
    M2C_FIELD(native_data_02101ae8, s32 *, 0xC84) = 1;
    return (u32) native_data_02101ae8;
}
