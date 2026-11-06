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
extern u32 native_fn_0203ca5c();
extern u32 native_fn_0203cb0c();
extern u32 native_fn_0203d0fc();
extern u32 native_fn_ov000_021e63c8();
extern u32 native_fn_ov000_0222a758();
typedef struct {
    u8 unknown_0[0x144];
    s8 field_144;
} Record_native_data_ov000_0223508c;
extern Record_native_data_ov000_0223508c native_data_ov000_0223508c;
u32 native_ov000_021e64e0(void) {
    u32 temp_r0;

    native_fn_0203ca5c(native_fn_ov000_021e63c8(-1), 0);
    temp_r0 = native_fn_0203d0fc();
    if (temp_r0 == 1) {
        native_fn_0203cb0c(0);
    } else if (temp_r0 == 2) {
        if (native_fn_ov000_0222a758() != 0) {
            native_data_ov000_0223508c.field_144 = 1;
        } else {
            native_data_ov000_0223508c.field_144 = 0;
        }
    }
    return 1U;
}
