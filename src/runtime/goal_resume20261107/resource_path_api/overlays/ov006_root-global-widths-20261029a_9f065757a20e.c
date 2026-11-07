#include "../resource_path_api.h"
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
extern u32 native_fn_0203cc2c();
extern u32 native_fn_02045654();
extern u32 native_fn_0204594c();
extern u8 native_data_ov006_0220d15c[];
u32 native_ov006_021e6bdc(s32 arg0) {
    u32 temp_r0;
    s32 temp_r4;
    u32 temp_r5;

    if (arg0 != -1) {
        temp_r4 = *(u32 *)(native_data_ov006_0220d15c + (arg0 * 4));
        temp_r5 = native_fn_0202a8e0((const void *)(u32)temp_r4);
        temp_r0 = native_fn_0203cc2c(temp_r4, 2);
        native_fn_0204594c(2, temp_r0, 0, temp_r5);
        return native_fn_0202a498(2, temp_r0);
    }
    return native_fn_02045654(2);
}
