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
extern u32 native_fn_ov006_021e8000();
extern u32 native_fn_ov006_021e8fc0();
extern u32 native_fn_ov006_021eb1b0();
extern u32 native_fn_ov006_02204f58();
typedef struct {
    s32 field_0;
    u32 field_4;
    s32 field_8;
} Record_native_data_ov006_0221c1f0;
extern Record_native_data_ov006_0221c1f0 native_data_ov006_0221c1f0;
u32 native_ov006_02205258(u32 arg0) {
    u32 temp_r0;
    u32 temp_r0_2;

    temp_r0 = native_fn_ov006_021e8fc0(native_data_ov006_0221c1f0.field_0, native_data_ov006_0221c1f0.field_8, arg0);
    if ((temp_r0 == 0) && (native_data_ov006_0221c1f0.field_0 != 0)) {
        temp_r0_2 = native_fn_ov006_021e8000();
        if ((temp_r0_2 != -1U) && (temp_r0_2 != native_data_ov006_0221c1f0.field_4)) {
            native_fn_ov006_02204f58(temp_r0_2, native_data_ov006_0221c1f0.field_8);
            native_fn_ov006_021eb1b0();
            native_data_ov006_0221c1f0.field_4 = temp_r0_2;
        }
    }
    return temp_r0;
}
