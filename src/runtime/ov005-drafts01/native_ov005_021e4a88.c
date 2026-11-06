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
extern u32 native_fn_02049604();
extern u32 native_fn_020bf0b0();
extern u32 native_fn_020bf218();
extern u32 native_fn_ov005_021da614();
extern u32 native_fn_ov005_021dd788();
extern u32 native_fn_ov005_021de19c();
extern u32 native_fn_ov005_021e0040();
extern u32 native_fn_ov005_021e026c();
extern u32 native_fn_ov005_021e0708();
extern u32 native_fn_ov005_021e0724();
extern u32 native_fn_ov005_021e0a68();
extern u32 native_fn_ov005_021e0a84();
extern u32 native_fn_ov005_021e0a90();
extern u32 native_fn_ov005_021e0d88();
extern u32 native_fn_ov005_021e1048();
extern u32 native_fn_ov005_021e155c();
typedef struct {
    u8 unknown_0[0x4];
    u8 field_4;
    u8 unknown_5[0x3];
    s8 field_8;
    u8 unknown_9[0xf];
    s32 field_18;
    u8 unknown_1c[0x24];
    s32 field_40;
    u8 unknown_44[0x20];
    s32 field_64;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
u32 native_ov005_021e4a88(void) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r4;

    temp_r0_2 = native_fn_ov005_021dd788();
    if (temp_r0_2 != 1) {
        return temp_r0_2;
    }
    native_fn_ov005_021e0040();
    if (M2C_FIELD((void *) native_fn_ov005_021e0a84(), u16 *, 2) & 1) {
        native_fn_ov005_021da614(0);
        native_data_ov005_021ed438.field_8 = (s8) native_fn_ov005_021e0a90();
        native_fn_ov005_021de19c(native_data_ov005_021ed438.field_8);
        native_fn_ov005_021e1048(0x52);
        native_fn_02048034(((u8) native_data_ov005_021ed438.field_8 * 0x268) + (native_data_ov005_021ed438.field_40 + 0x100), 0);
        native_fn_ov005_021e0708(0x13, 2, 0x11);
        native_fn_ov005_021e0724(1);
        return native_fn_ov005_021e155c(0x3A);
    }
    if (M2C_FIELD((void *) native_fn_ov005_021e0a84(), u16 *, 2) & 2) {
        native_fn_ov005_021e1048(0x53);
        if (native_data_ov005_021ed438.field_64 == 0xD) {
            native_data_ov005_021ed438.field_18 = 0;
            native_fn_ov005_021e155c(0xD);
            native_fn_ov005_021e026c(3, 1, 0, 0x10, 0, 0);
            native_fn_ov005_021e1048(0x52);
            return native_fn_020bf0b0(native_data_ov005_021ed438.field_4);
        }
        native_data_ov005_021ed438.field_8 = (s8) native_fn_ov005_021e0a90();
        native_fn_02048034(native_fn_020bf218() + 0xB0, 0);
        native_fn_ov005_021e0708(0x13, 2, 0x12);
        return native_fn_ov005_021e155c(0x37);
    }
    temp_r4 = native_fn_ov005_021e0a90();
    native_fn_ov005_021e0d88();
    temp_r0 = native_fn_ov005_021e0a90();
    if (temp_r4 == temp_r0) {
        return temp_r0;
    }
    return native_fn_02049604(native_fn_ov005_021e0a68(), 1);
}
