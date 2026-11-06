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
extern u32 native_fn_020d3540(s32 value);
typedef struct {
    s32 field_0;
    s32 field_4;
    s32 field_8;
} Record_native_data_020e32f4;
extern Record_native_data_020e32f4 native_data_020e32f4;
u32 native_main_020d3f4c(u32 arg0, u32 arg1) {
    u32 temp_r0;
    u32 var_r4;
    u32 temp_r5;

    var_r4 = 0;
    temp_r5 = native_fn_020d3540((s32)arg0);
    temp_r0 = native_fn_020d3540((s32)arg1);
    if ((native_data_020e32f4.field_4 & temp_r5) && (native_data_020e32f4.field_4 & temp_r0)) {
        var_r4 |= 1;
    }
    if ((native_data_020e32f4.field_8 & temp_r5) && (native_data_020e32f4.field_8 & temp_r0)) {
        var_r4 |= 2;
    }
    if ((native_data_020e32f4.field_0 & temp_r5) && (native_data_020e32f4.field_0 & temp_r0)) {
        var_r4 |= 4;
    }
    return var_r4;
}
