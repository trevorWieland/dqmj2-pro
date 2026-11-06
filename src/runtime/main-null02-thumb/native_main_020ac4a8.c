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
extern u32 native_fn_020a8614();
extern u32 native_fn_020a929c();
extern u32 native_fn_020ac480();
extern u32 native_fn_020ac6f4();
extern u32 native_fn_020ac710();
extern u32 native_fn_020b0a50();
extern u32 native_fn_020b0b48();
extern u32 native_fn_020b0bd0();
extern u32 native_fn_020b0ca8();
extern u32 native_fn_020b2c88();
extern u8 native_data_020e05f8[];
extern u8 native_data_020e061c[];
extern u8 native_data_020e0768[];
extern u8 native_data_020e07a8[];
extern u8 native_data_020e07b4[];
u32 native_main_020ac4a8(void **arg0, u32 arg1, s32 arg2) {
    void *temp_r0;
    void *temp_r0_2;
    void *temp_r4;
    s32 temp_r6;
    s32 temp_r6_2;
    void *sp0;

    temp_r4 = *arg0;
    if (native_fn_020b0a50(arg0, arg1, &sp0) == 0) {
        native_fn_020b2c88(arg0, native_data_020e0768);
        return 2U;
    }
    if (arg2 == 1) {
        native_fn_020ac6f4(arg0, temp_r4 + 0x210, native_data_020e07a8);
        native_fn_020ac6f4(arg0, temp_r4 + 0x210, native_data_020e05f8);
        native_fn_020ac710(arg0, temp_r4 + 0x210, M2C_FIELD(temp_r4, s32 *, 0x198));
        native_fn_020ac6f4(arg0, temp_r4 + 0x210, native_data_020e07b4);
        native_fn_020ac710(arg0, temp_r4 + 0x210, M2C_FIELD(sp0, s32 *, 0));
        native_fn_020ac6f4(arg0, temp_r4 + 0x210, native_data_020e061c);
    }
    temp_r0 = M2C_FIELD(sp0, void **, 8);
    if (temp_r0 != NULL) {
        temp_r6 = M2C_FIELD(temp_r0, s32 *, 0);
        native_fn_020a929c(M2C_FIELD(temp_r0, void **, 8));
        M2C_FIELD(M2C_FIELD(sp0, void **, 8), s32 *, 8) = 0;
        native_fn_020a929c(M2C_FIELD(M2C_FIELD(sp0, void **, 8), void **, 0xC));
        M2C_FIELD(M2C_FIELD(sp0, void **, 8), s32 *, 0xC) = 0;
        native_fn_020a929c(M2C_FIELD(sp0, void **, 8));
        M2C_FIELD(sp0, void **, 8) = NULL;
        if (native_fn_020b0ca8(sp0) != 0) {
            native_fn_020b0b48(arg0, sp0);
        }
        M2C_FIELD(temp_r4, s32 *, 0x5D0) = (s32) (M2C_FIELD(temp_r4, s32 *, 0x5D0) - 1);
        native_fn_020b0bd0(arg0, native_fn_020ac480, temp_r6);
    }
    temp_r0_2 = M2C_FIELD(sp0, void **, 0xC);
    if (temp_r0_2 != NULL) {
        temp_r6_2 = M2C_FIELD(temp_r0_2, s32 *, 0);
        native_fn_020a929c(M2C_FIELD(temp_r0_2, void **, 8));
        M2C_FIELD(M2C_FIELD(sp0, void **, 0xC), s32 *, 8) = 0;
        native_fn_020a929c(M2C_FIELD(M2C_FIELD(sp0, void **, 0xC), void **, 0xC));
        M2C_FIELD(M2C_FIELD(sp0, void **, 0xC), s32 *, 0xC) = 0;
        native_fn_020a929c(M2C_FIELD(M2C_FIELD(sp0, void **, 0xC), void **, 0x10));
        M2C_FIELD(M2C_FIELD(sp0, void **, 0xC), s32 *, 0x10) = 0;
        native_fn_020a929c(M2C_FIELD(M2C_FIELD(sp0, void **, 0xC), void **, 0x14));
        M2C_FIELD(M2C_FIELD(sp0, void **, 0xC), s32 *, 0x14) = 0;
        native_fn_020a929c(M2C_FIELD(sp0, void **, 0xC));
        M2C_FIELD(sp0, void **, 0xC) = NULL;
        if (M2C_FIELD(M2C_FIELD(sp0, void **, 0xC), s32 *, 0x38) != 0) {
            native_fn_020a8614();
            M2C_FIELD(M2C_FIELD(sp0, void **, 0xC), s32 *, 0x38) = 0;
        }
        if (native_fn_020b0ca8(sp0) != 0) {
            native_fn_020b0b48(arg0, sp0);
        }
        M2C_FIELD(temp_r4, s32 *, 0x5D0) = (s32) (M2C_FIELD(temp_r4, s32 *, 0x5D0) - 1);
        native_fn_020b0bd0(arg0, native_fn_020ac480, temp_r6_2);
    }
    return 0U;
}
