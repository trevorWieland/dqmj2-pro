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
extern u32 native_fn_ov001_021d732c();
extern u32 native_fn_ov001_021d7564();
extern u32 native_fn_ov001_021e35b4();
extern u8 native_data_ov001_0222f158[];
typedef struct {
    u8 unknown_0[0x1];
    u8 field_1;
    u8 unknown_2[0x1];
    s8 field_3;
} Record_native_data_ov001_0223e088;
extern Record_native_data_ov001_0223e088 native_data_ov001_0223e088;
u32 native_ov001_0220b808(void) {
    if (native_data_ov001_0223e088.field_1 == 0) {
        native_fn_ov001_021d732c(0x2D, 2);
        native_fn_ov001_021d7564(0x2D, native_data_ov001_0222f158, 0);
        native_data_ov001_0223e088.field_1 = 0xAU;
    }
    else if (native_data_ov001_0223e088.field_1 == 10) {
        native_fn_ov001_021e35b4(0x18);
        native_data_ov001_0223e088.field_1 = 0x14U;
    }
    else if (native_data_ov001_0223e088.field_1 == 20) {
        native_fn_ov001_021e35b4(0x19);
        native_data_ov001_0223e088.field_1 = 0x64U;
    }

    if (native_data_ov001_0223e088.field_1 == 0x64) {
        native_data_ov001_0223e088.field_1 = 0U;
        native_data_ov001_0223e088.field_3 = 2;
    }
    return 0U;
}
