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
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u32 native_fn_0208a060();
typedef struct {
    u8 unknown_0[0x2c];
    s32 field_2c;
} Record_native_data_ov006_0221aad0;
extern Record_native_data_ov006_0221aad0 native_data_ov006_0221aad0;
u32 native_ov006_021eee44(void) {
    u32 temp_r4;

    temp_r4 = native_fn_02007ff4();
    if ((native_data_ov006_0221aad0.field_2c == 7) && (native_fn_0208a060() == 3)) {
        native_data_ov006_0221aad0.field_2c = 4;
        native_fn_02008008(temp_r4);
        return 1U;
    }
    native_fn_02008008(temp_r4);
    return 0U;
}
