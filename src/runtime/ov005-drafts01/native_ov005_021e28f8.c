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
extern u32 native_fn_020bf084();
extern u32 native_fn_020bf148();
extern u32 native_fn_ov005_021dd788();
extern u32 native_fn_ov005_021ddf24();
extern u32 native_fn_ov005_021de1bc();
extern u32 native_fn_ov005_021e00b4();
extern u32 native_fn_ov005_021e026c();
extern u32 native_fn_ov005_021e0818();
extern u32 native_fn_ov005_021e0a84();
extern u32 native_fn_ov005_021e155c();
typedef struct {
    u8 unknown_0[0x4];
    u8 field_4;
    u8 unknown_5[0x13];
    s32 field_18;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
u32 native_ov005_021e28f8(void) {
    u32 temp_r0;

    temp_r0 = native_fn_ov005_021dd788();
    if (temp_r0 != 1) {
        return temp_r0;
    }
    if (!(M2C_FIELD((void *) native_fn_ov005_021e0a84(), u16 *, 2) & 0xFF7)) {
        return 0xFF7U;
    }
    native_fn_ov005_021e0818();
    native_fn_020bf148(native_data_ov005_021ed438.field_4);
    native_fn_ov005_021de1bc(0);
    if (native_fn_020bf084() == 0) {
        native_fn_ov005_021e155c(0);
        native_fn_ov005_021e00b4(0, 0, 0, 0);
        native_fn_ov005_021e026c(4U, 0, 0, 1, 0, 0);
        return native_fn_ov005_021ddf24();
    }
    native_data_ov005_021ed438.field_4 = 0xFFU;
    native_data_ov005_021ed438.field_18 = 1;
    native_fn_ov005_021e026c(native_fn_020bf084(), 0, 0, 1, 0, 0);
    return native_fn_ov005_021e155c(0xC);
}
