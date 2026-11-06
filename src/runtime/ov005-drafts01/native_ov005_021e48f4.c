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
extern u32 native_fn_02048034();
extern u32 native_fn_020bf218();
extern u32 native_fn_ov005_021e00b4();
extern u32 native_fn_ov005_021e026c();
extern u32 native_fn_ov005_021e0730();
extern u32 native_fn_ov005_021e0818();
extern u32 native_fn_ov005_021e0838();
extern u32 native_fn_ov005_021e0a84();
extern u32 native_fn_ov005_021e0aa0();
extern u32 native_fn_ov005_021e1048();
extern u32 native_fn_ov005_021e155c();
typedef struct {
    u8 unknown_0[0x8];
    u8 field_8;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
u32 native_ov005_021e48f4(void) {
    u16 temp_r0;

    native_fn_ov005_021e0838();
    if (M2C_FIELD((void *) native_fn_ov005_021e0a84(), u16 *, 2) & 1) {
        native_fn_ov005_021e0818();
        native_fn_ov005_021e1048(0x52);
        if (native_fn_ov005_021e0aa0() == 0) {
            native_fn_ov005_021e0818();
            native_fn_ov005_021e1048(0x53);
            native_fn_02048034(native_fn_020bf218() + 0xB0, 0);
            native_fn_ov005_021e0730(0x13, 2, 0x13);
            native_fn_ov005_021e155c(0x3C);
        } else {
            native_fn_ov005_021e00b4(0x13, 0, 8, 1);
            native_fn_ov005_021e026c(8, native_data_ov005_021ed438.field_8, 0, 0, 0, 2);
            native_fn_ov005_021e155c(0x39);
        }
    }
    temp_r0 = M2C_FIELD((void *) native_fn_ov005_021e0a84(), u16 *, 2);
    if (!(temp_r0 & 2)) {
        return (u32) temp_r0;
    }
    native_fn_ov005_021e0818();
    native_fn_ov005_021e1048(0x53);
    native_fn_ov005_021e00b4(0x13, 0, 8, 1);
    native_fn_ov005_021e026c(8, native_data_ov005_021ed438.field_8, 0, 0, 0, 2);
    return native_fn_ov005_021e155c(0x39);
}
