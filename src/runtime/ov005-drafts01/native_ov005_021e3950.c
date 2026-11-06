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
extern u32 native_fn_02041800();
extern u32 native_fn_0206dcd0();
extern u32 native_fn_ov005_021dd680();
extern u32 native_fn_ov005_021dd788();
extern u32 native_fn_ov005_021e00b4();
extern u32 native_fn_ov005_021e026c();
extern u32 native_fn_ov005_021e0a84();
extern u32 native_fn_ov005_021e0a90();
extern u32 native_fn_ov005_021e0d88();
extern u32 native_fn_ov005_021e155c();
typedef struct {
    u8 unknown_0[0x4];
    u8 field_4;
    u8 unknown_5[0x17];
    u32 field_1c;
    u8 unknown_20[0x20];
    s32 field_40;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
u32 native_ov005_021e3950(void) {
    u16 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;

    temp_r0_3 = native_fn_ov005_021dd788();
    if (temp_r0_3 != 0x16) {
        return temp_r0_3;
    }
    temp_r0_2 = native_fn_02041800();
    if (temp_r0_2 == 1) {
        return temp_r0_2;
    }
    native_fn_ov005_021e0d88();
    if (native_data_ov005_021ed438.field_1c != native_fn_ov005_021e0a90()) {
        native_data_ov005_021ed438.field_1c = native_fn_ov005_021e0a90();
        native_fn_0206dcd0((0x84 * native_fn_ov005_021e0a90()) + ((native_data_ov005_021ed438.field_4 * 0x268) + (native_data_ov005_021ed438.field_40 + 0x114)));
    }
    temp_r0 = M2C_FIELD((void *) native_fn_ov005_021e0a84(), u16 *, 2);
    if (!(temp_r0 & 2)) {
        return (u32) temp_r0;
    }
    native_fn_ov005_021e155c(0x23);
    native_fn_ov005_021e00b4(0x13, native_data_ov005_021ed438.field_4, 0, 2);
    native_fn_ov005_021e026c(3, 1, 0, 0x16, 0, 2);
    return native_fn_ov005_021dd680();
}
