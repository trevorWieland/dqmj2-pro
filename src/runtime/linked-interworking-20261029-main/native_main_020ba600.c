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
extern u32 native_fn_0209bb10();
extern u32 native_fn_020ba5b0();
typedef struct {
    u8 unknown_0[0xc];
    s32 field_c;
    u8 unknown_10[0xc];
    s32 field_1c;
    u8 unknown_20[0x14];
    s32 field_34;
} Record_native_data_021d3044;
extern Record_native_data_021d3044 native_data_021d3044;
u32 native_main_020ba600(u32 arg0, s32 arg1, s32 arg2) {
    s32 var_r4;

    var_r4 = arg2;
    if ((native_data_021d3044.field_c == 4) && (native_fn_0209bb10(native_fn_020ba5b0, arg0) != 0)) {
        if (var_r4 == 0) {
            var_r4 = 0x2710;
        }
        native_data_021d3044.field_1c = arg1;
        native_data_021d3044.field_34 = var_r4;
        return 1U;
    }
    return 0U;
}
