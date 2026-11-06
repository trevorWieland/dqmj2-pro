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
extern u32 native_fn_0205caf4();
extern u32 native_fn_0205ce38();
typedef struct {
    u8 field_0;
    u8 unknown_1[0x7];
    s32 field_8;
    s32 field_c;
    s32 field_10;
} Record_native_data_ov000_022351d4;
extern Record_native_data_ov000_022351d4 native_data_ov000_022351d4;
u32 native_ov000_021e75b4(void) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;
    u32 var_r4;

    var_r4 = 0;
    switch (native_data_ov000_022351d4.field_0) {
    default:
        break;
    case 1:
        var_r4 = native_fn_0205caf4(0xF8, native_data_ov000_022351d4.field_8, native_data_ov000_022351d4.field_c, native_data_ov000_022351d4.field_10);
        break;
    case 2:
        temp_r0 = native_fn_0205caf4(0x102, native_data_ov000_022351d4.field_8, native_data_ov000_022351d4.field_c, native_data_ov000_022351d4.field_10);
        var_r4 = temp_r0;
        native_fn_0205ce38(temp_r0, 0x6000);
        break;
    case 3:
        temp_r0_2 = native_fn_0205caf4(0x103, native_data_ov000_022351d4.field_8, native_data_ov000_022351d4.field_c, native_data_ov000_022351d4.field_10);
        var_r4 = temp_r0_2;
        native_fn_0205ce38(temp_r0_2, 0x6000);
        break;
    case 4:
        temp_r0_3 = native_fn_0205caf4(0x104, native_data_ov000_022351d4.field_8, native_data_ov000_022351d4.field_c, native_data_ov000_022351d4.field_10);
        var_r4 = temp_r0_3;
        native_fn_0205ce38(temp_r0_3, 0x6000);
        break;
    }
    return var_r4;
}
