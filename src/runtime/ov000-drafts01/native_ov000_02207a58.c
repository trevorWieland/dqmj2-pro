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
extern u32 native_fn_0202a498();
extern u32 native_fn_020484dc();
extern u32 native_fn_020485b4();
extern u32 native_fn_0205f920();
typedef struct {
    u8 unknown_0[0xf2];
    u8 field_f2;
    u8 unknown_f3[0x15];
    s32 field_108;
    u8 unknown_10c[0xc];
    s32 field_118;
} Record_native_data_ov000_022382c8;
extern Record_native_data_ov000_022382c8 native_data_ov000_022382c8;
u32 native_ov000_02207a58(void) {
    if (native_data_ov000_022382c8.field_118 != 0) {
        native_fn_0205f920(native_data_ov000_022382c8.field_118, 1, 2);
        native_fn_0202a498(2, native_data_ov000_022382c8.field_118);
        native_data_ov000_022382c8.field_118 = 0;
    }
    if (native_data_ov000_022382c8.field_108 != 0) {
        native_fn_020485b4();
        native_data_ov000_022382c8.field_108 = 0;
    }
    return native_fn_020484dc(1, native_data_ov000_022382c8.field_f2);
}
