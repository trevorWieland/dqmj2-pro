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
extern u8 native_data_020e68c0[];
u32 native_main_02016690(void *arg0) {
    void *var_r1;
    void *var_r2;

    var_r2 = M2C_FIELD(native_data_020e68c0, void **, 0x18);
    if (var_r2 == NULL) {
        M2C_FIELD(native_data_020e68c0, void **, 0x18) = arg0;
    } else {
        var_r1 = M2C_FIELD(var_r2, void **, 0x4BC);
        if (var_r1 != NULL) {
            do {
                var_r2 = var_r1;
                var_r1 = M2C_FIELD(var_r1, void **, 0x4BC);
            } while (var_r1 != NULL);
        }
        M2C_FIELD(var_r2, void **, 0x4BC) = arg0;
    }
    M2C_FIELD(arg0, s32 *, 0x4BC) = 0;
    return (u32) arg0;
}
