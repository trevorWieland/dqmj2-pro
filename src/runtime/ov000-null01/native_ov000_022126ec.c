#define NULL ((void *)0)
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
typedef struct {
    s16 field_0;
    s16 field_2;
} Record_native_data_ov000_02240c74;
extern Record_native_data_ov000_02240c74 native_data_ov000_02240c74;
u32 native_ov000_022126ec(s16 *arg0, s16 *arg1) {
    u32 var_ip;

    var_ip = 0;
    if ((arg0 != NULL) && (arg1 != NULL)) {
        var_ip = 1;
        *arg0 = native_data_ov000_02240c74.field_0;
        *arg1 = native_data_ov000_02240c74.field_2;
    }
    return var_ip;
}
