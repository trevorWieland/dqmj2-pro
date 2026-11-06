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
extern u32 native_fn_02041f74();
extern u32 native_fn_02042c2c();
extern u32 native_fn_ov001_021d75d4();
extern u32 native_fn_ov001_021d77b0();
extern u32 native_fn_ov001_021d7814();
extern u32 native_fn_ov001_021d94cc();
extern u32 native_fn_ov001_021dba58();
extern u32 native_fn_ov001_021dbac8();
typedef struct {
    u8 unknown_0[0x40];
    s32 field_40;
} Record_native_data_ov001_02239a14;
extern Record_native_data_ov001_02239a14 native_data_ov001_02239a14;
u32 native_ov001_021fad98(void) {
    u32 temp_r4;
    u32 temp_r5;

    temp_r5 = native_fn_ov001_021dba58(1, 2);
    temp_r4 = native_fn_ov001_021dba58(1, 1);
    if (native_fn_ov001_021dbac8(1) != 0) {
        native_fn_ov001_021d75d4(0x11);
    } else if (temp_r5 != 0) {
        native_fn_ov001_021d75d4(0x10);
    } else if (temp_r4 != 0) {
        native_fn_ov001_021d75d4(0xF);
    } else {
        native_fn_ov001_021d75d4(0xE);
    }
    native_fn_ov001_021d94cc(0, 1);
    native_fn_ov001_021d77b0(-1, native_fn_02042c2c(native_data_ov001_02239a14.field_40));
    return native_fn_ov001_021d7814(-1, native_fn_02041f74(native_data_ov001_02239a14.field_40, 0));
}
