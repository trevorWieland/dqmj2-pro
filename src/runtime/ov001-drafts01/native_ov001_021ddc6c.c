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
extern u32 native_fn_ov001_021d75d4();
extern u32 native_fn_ov001_021d94cc();
extern u32 native_fn_ov001_021dccd0();
extern u32 native_fn_ov001_021e7dfc();
extern u32 native_fn_ov001_021e7f3c();
extern u32 native_fn_ov001_02210d98();
extern u32 native_fn_ov001_02210e08();
extern u32 native_fn_ov001_02210e18();
typedef struct {
    u8 unknown_0[0x3];
    u8 field_3;
    u8 unknown_4[0x2];
    s8 field_6;
    u8 field_7;
    s8 field_8;
    u8 unknown_9[0x2f];
    s32 field_38;
} Record_native_data_ov001_022388ec;
extern Record_native_data_ov001_022388ec native_data_ov001_022388ec;
u32 native_ov001_021ddc6c(void) {
    u32 var_r4;

    var_r4 = 0;
    if (native_data_ov001_022388ec.field_3 == 0) {
        if (native_data_ov001_022388ec.field_7 == 0) {
            native_fn_ov001_021e7dfc();
        } else {
            native_fn_ov001_021e7f3c();
        }
        native_fn_ov001_021dccd0(0);
        native_fn_ov001_021d75d4(2);
        native_fn_ov001_021d94cc(0, 1);
        native_fn_ov001_02210d98();
        native_data_ov001_022388ec.field_3 = 0xAU;
    }
    if ((native_data_ov001_022388ec.field_3 == 0xA) && (native_fn_ov001_02210e08() == 2)) {
        native_data_ov001_022388ec.field_3 = 0x14U;
    }
    if (native_data_ov001_022388ec.field_3 == 0x14) {
        native_fn_ov001_02210e18();
        native_data_ov001_022388ec.field_3 = 0x64U;
    }
    if (native_data_ov001_022388ec.field_3 == 0x64) {
        native_data_ov001_022388ec.field_38 = 0;
        native_data_ov001_022388ec.field_8 = 2;
        var_r4 = 1;
        native_data_ov001_022388ec.field_6 = 1;
        native_data_ov001_022388ec.field_3 = 0U;
    }
    return var_r4;
}
