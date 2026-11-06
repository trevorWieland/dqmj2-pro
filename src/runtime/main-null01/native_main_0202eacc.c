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
extern u32 native_fn_0202e9ac();
extern u32 native_fn_0202ea64();
u32 native_main_0202eacc(u8 *arg0, void *arg1) {
    u8 *var_r0;
    u8 temp_r0;
    u8 *temp_r5;

    var_r0 = arg0;
    temp_r5 = var_r0;
    if ((arg1 != NULL) && (var_r0 = M2C_FIELD(arg1, u8 **, 8), (var_r0 != NULL))) {
        temp_r0 = *var_r0;
        switch (temp_r0) {
        default:
            return (u32) temp_r0;
        case 0x4D:
            native_fn_0202ea64(temp_r5 + 0x3C);
            return native_fn_0202e9ac(temp_r5 + 8, arg1);
        case 0x4A:
            native_fn_0202ea64(temp_r5 + 0x44);
            return native_fn_0202e9ac(temp_r5 + 0x10, arg1);
        case 0x56:
            native_fn_0202ea64(temp_r5 + 0x4C);
            return native_fn_0202e9ac(temp_r5 + 0x18, arg1);
        }
    } else {
        return (u32) var_r0;
    }
}
