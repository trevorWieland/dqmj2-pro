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
extern u32 native_fn_020a8b6c();
extern u32 native_fn_020a8b7c();
extern u32 native_fn_020a929c();
extern u32 native_fn_020b3680();
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
} Record_native_data_020e15f0;
extern Record_native_data_020e15f0 native_data_020e15f0;
extern u8 native_data_021d2514[];
u32 native_main_020b3068(void) {
    u8 *var_r0;

    if (native_data_020e15f0.field_4 != -1) {
        native_fn_020a8b7c(native_data_020e15f0.field_4, 2);
        native_fn_020a8b6c(native_data_020e15f0.field_4);
    }
    native_data_020e15f0.field_4 = -1;
    native_fn_020b3680();
    var_r0 = M2C_FIELD(native_data_021d2514, u8 **, 0x28);
    if (var_r0 != NULL) {
        native_fn_020a929c();
        var_r0 = native_data_021d2514;
        M2C_FIELD(native_data_021d2514, u8 **, 0x28) = NULL;
        M2C_FIELD(native_data_021d2514, s32 *, 0x18) = 0;
        M2C_FIELD(native_data_021d2514, s32 *, 8) = 0;
    }
    return (u32) var_r0;
}
