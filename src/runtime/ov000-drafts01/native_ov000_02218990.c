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
extern u32 native_fn_0203cc2c();
extern u8 native_data_ov000_0222fabc[];
typedef struct {
    u8 unknown_0[0x4];
    u32 field_4;
} Record_native_data_ov000_02245e54;
extern Record_native_data_ov000_02245e54 native_data_ov000_02245e54;
u32 native_ov000_02218990(void) {
    u32 temp_r0;

    temp_r0 = native_fn_0203cc2c(native_data_ov000_0222fabc, 2);
    native_data_ov000_02245e54.field_4 = temp_r0;
    return temp_r0;
}
