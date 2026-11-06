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
extern u32 native_fn_0209cba8();
extern u32 native_fn_020aa5f8();
extern u8 native_data_021d1b74[];
u32 native_main_0209d1c8(s32 arg0, s32 arg1, s32 arg2) {
    s32 var_r4;
    s32 var_r5;
    s32 var_r6;

    var_r5 = arg0;
    var_r4 = arg1;
    var_r6 = arg2;
    if ((M2C_FIELD(native_data_021d1b74, void **, 0xC) == NULL) || (native_fn_0209cba8() == 0)) {
        return 0U;
    }
    if (var_r5 == -1) {
        var_r5 = M2C_FIELD(*M2C_FIELD(M2C_FIELD(native_data_021d1b74, void **, 0xC), void ***, 4), s32 *, 0x23C);
    }
    if (var_r4 == 0) {
        var_r4 = *M2C_FIELD(M2C_FIELD(native_data_021d1b74, void **, 0xC), void ***, 4) + 0x3B8;
    }
    if (var_r6 == 0) {
        var_r6 = *M2C_FIELD(M2C_FIELD(native_data_021d1b74, void **, 0xC), void ***, 4) + 0x4B8;
    }
    return native_fn_020aa5f8(M2C_FIELD(M2C_FIELD(native_data_021d1b74, void **, 0xC), void ***, 4), var_r5, var_r4, var_r6);
}
