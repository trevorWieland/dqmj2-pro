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
extern u32 native_fn_02003888();
extern u32 native_fn_02003e44();
extern u32 native_fn_0202a37c();
extern u32 native_fn_0202a498();
typedef struct {
    s32 field_0;
    u32 field_4;
    u32 field_8;
    u32 field_c;
} Record_native_data_ov000_02246428;
extern Record_native_data_ov000_02246428 native_data_ov000_02246428;
u32 native_ov000_022214ac(void) {
    u32 var_r4;

    var_r4 = 0;
    if (native_data_ov000_02246428.field_0 != 0) {
        if (native_data_ov000_02246428.field_8 == 0) {
            native_data_ov000_02246428.field_8 = native_fn_0202a37c(1, 0x18000, 4);
        }
        if (native_data_ov000_02246428.field_4 == 0) {
            native_data_ov000_02246428.field_4 = native_fn_0202a37c(1, 0x18000, 4);
        }
        if (native_data_ov000_02246428.field_8 != 0) {
            if (native_data_ov000_02246428.field_4 != 0) {
                native_data_ov000_02246428.field_c = native_fn_02003e44();
                native_fn_02003888(4);
                var_r4 = 1;
                *(s32 *)0x04000064 = 0x81320010;
            } else {
                native_fn_0202a498(1);
            }
        }
    }
    return var_r4;
}
