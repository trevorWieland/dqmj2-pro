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
extern u32 native_fn_02041538();
extern u32 native_fn_02044ff4();
extern u32 native_fn_02048034();
extern u32 native_fn_020642cc();
extern u32 native_fn_020642dc();
extern u32 native_fn_020642f8();
extern u32 native_fn_ov005_021dd788();
extern u32 native_fn_ov005_021dd798();
extern u32 native_fn_ov005_021ddf24();
extern u32 native_fn_ov005_021e0730();
extern u32 native_fn_ov005_021e0818();
extern u32 native_fn_ov005_021e0838();
extern u32 native_fn_ov005_021e0a84();
extern u32 native_fn_ov005_021e0aa0();
extern u32 native_fn_ov005_021e1048();
extern u32 native_fn_ov005_021e155c();
typedef struct {
    u8 unknown_0[0x38];
    s32 field_38;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
u32 native_ov005_021e4570(void) {
    u16 temp_r0;
    u32 temp_r0_2;
    u8 sp0[32];

    temp_r0_2 = native_fn_ov005_021dd788();
    if (temp_r0_2 != 1) {
        return temp_r0_2;
    }
    native_fn_ov005_021e0838();
    temp_r0 = M2C_FIELD((void *) native_fn_ov005_021e0a84(), u16 *, 2);
    if (!(temp_r0 & 1)) {
        return (u32) temp_r0;
    }
    native_fn_ov005_021e0818();
    native_fn_ov005_021e1048(0x52);
    if (native_fn_ov005_021e0aa0() == 0) {
        native_fn_ov005_021e155c(0x3D);
        native_data_ov005_021ed438.field_38 = 3;
        native_fn_ov005_021dd798();
        return native_fn_02041538(1, 2, 0x1E);
    }
    native_fn_ov005_021ddf24();
    native_fn_02044ff4(&sp0, M2C_FIELD((void *) native_fn_020642f8(), u16 *, 2), 0);
    native_fn_02048034(&sp0, 0);
    native_fn_ov005_021e0730(0x13, 2, 0x2A);
    native_fn_ov005_021e155c(0x1B);
    if (native_fn_020642dc() == 0x32) {
        native_fn_ov005_021e155c(0x34);
    }
    return native_fn_020642cc(0);
}
