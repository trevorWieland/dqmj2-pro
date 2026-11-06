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
extern u32 native_fn_02041538();
extern u32 native_fn_ov001_02201d4c();
extern u32 native_fn_ov001_022023f8();
extern u32 native_fn_ov001_022068a0();
typedef struct {
    u8 unknown_0[0xa];
    s8 field_a;
} Record_native_data_ov001_02239c10;
extern Record_native_data_ov001_02239c10 native_data_ov001_02239c10;
u32 native_ov001_02201d74(void) {
    u32 var_r4;

    var_r4 = 0;
    native_fn_ov001_022068a0();
    if (native_fn_ov001_022023f8(0x200) != 0) {
        native_data_ov001_02239c10.field_a = 0x12;
        native_fn_02041538(0, 2, 0xA);
    } else if (native_fn_ov001_022023f8(0x400) != 0) {
        var_r4 = native_fn_ov001_02201d4c();
    }
    return var_r4;
}
