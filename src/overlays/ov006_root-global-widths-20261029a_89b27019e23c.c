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
extern u32 native_fn_02062a10();
extern u32 native_fn_ov006_021eacf8();
extern u8 native_data_ov006_0221c290[];
u32 native_ov006_02206328(s32 arg0, s32 arg1) {
    u32 var_r2;

    var_r2 = 0;
    if ((arg0 >= 0) && (arg0 < 4) && (arg1 >= 0) && (arg1 < 3)) {
        var_r2 = native_fn_02062a10(*(u32 *)(native_data_ov006_0221c290 + ((arg0 + (arg1 * 4)) * 4)));
    }
    return native_fn_ov006_021eacf8(var_r2);
}
