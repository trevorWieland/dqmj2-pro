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
extern u32 native_fn_02008d78();
extern u32 native_fn_020966c8();
extern u32 native_fn_0209aa38();
typedef struct {
    u32 field_0;
    u32 field_4;
    s32 field_8;
} Record_native_data_021d18e4;
extern Record_native_data_021d18e4 native_data_021d18e4;
u32 native_main_02096900(s32 arg0, s32 arg1) {
    u32 temp_r0;

    native_data_021d18e4.field_4 = native_fn_0209aa38(1, native_fn_020966c8());
    temp_r0 = native_fn_0209aa38(1, 0x794U);
    native_data_021d18e4.field_0 = temp_r0;
    native_fn_02008d78(temp_r0, 0, 0x794);
    M2C_FIELD(native_data_021d18e4.field_0, s32 *, 0) = arg0;
    M2C_FIELD(native_data_021d18e4.field_0, s32 *, 0x790) = arg1;
    native_data_021d18e4.field_8 = 0;
    return 1U;
}
