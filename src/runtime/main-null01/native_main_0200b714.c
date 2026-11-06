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
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u32 native_fn_0200b16c();
extern u32 native_fn_0200b6d4();
extern u8 native_data_020e5348[];
u32 native_main_0200b714(void *arg0, u32 arg1, u32 arg2) {
    void *var_r0;
    void *var_r1;
    u32 temp_r4;
    u32 var_r8;

    var_r8 = 0;
    temp_r4 = native_fn_02007ff4();
    if (native_fn_0200b6d4(arg1, arg2) == 0) {
        var_r1 = M2C_FIELD(native_data_020e5348, void **, 0);
        if (var_r1 == NULL) {
            M2C_FIELD(native_data_020e5348, void **, 0) = arg0;
            M2C_FIELD(native_data_020e5348, void **, 4) = arg0;
            M2C_FIELD(native_data_020e5348, s32 *, 0xC) = 0;
            M2C_FIELD(native_data_020e5348, s16 *, 0xA) = 0;
            M2C_FIELD(native_data_020e5348, s16 *, 8) = 0;
        } else {
            var_r0 = M2C_FIELD(var_r1, void **, 4);
            if (var_r0 != NULL) {
                do {
                    var_r1 = var_r0;
                    var_r0 = M2C_FIELD(var_r0, void **, 4);
                } while (var_r0 != NULL);
            }
            M2C_FIELD(var_r1, void **, 4) = arg0;
            M2C_FIELD(arg0, void **, 8) = var_r1;
        }
        M2C_FIELD(arg0, u32 *, 0) = native_fn_0200b16c(arg1, arg2);
        var_r8 = 1;
        M2C_FIELD(arg0, s32 *, 0x1C) = (s32) (M2C_FIELD(arg0, s32 *, 0x1C) | 1);
    }
    native_fn_02008008(temp_r4);
    return var_r8;
}
