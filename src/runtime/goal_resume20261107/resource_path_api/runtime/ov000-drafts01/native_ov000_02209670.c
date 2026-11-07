#include "../../resource_path_api.h"
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
extern u32 native_fn_0201d444();
extern u32 native_fn_0203cc2c();
extern u8 native_data_ov000_0222f7e8[];
typedef struct {
    u8 unknown_0[0x8];
    u32 field_8;
} Record_native_data_ov000_02238514;
extern Record_native_data_ov000_02238514 native_data_ov000_02238514;
u32 native_ov000_02209670(void) {
    u8 sp0[20];
    u32 temp_r0;

    native_fn_0201d444(&sp0, native_data_ov000_0222f7e8);
    native_fn_0202a8e0(&sp0);
    temp_r0 = native_fn_0203cc2c(&sp0, 1);
    native_data_ov000_02238514.field_8 = temp_r0;
    if (temp_r0 != 0) {
        return 1U;
    }
    return 0U;
}
