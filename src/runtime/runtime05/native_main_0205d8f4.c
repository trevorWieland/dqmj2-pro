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
extern u8 native_data_021043ac[];
u32 native_main_0205d8f4(u32 arg0, u32 arg1) {
    s32 temp_r2;
    u32 *temp_r0;
    u32 var_ip;

    var_ip = -1U;
    if (arg0 < 0x20U) {
        temp_r2 = arg0 * 0x11C;
        if (*(native_data_021043ac + temp_r2) == 3) {
            temp_r0 = M2C_FIELD((native_data_021043ac + temp_r2), u32 **, 0x74);
            var_ip = *temp_r0;
            *temp_r0 = arg1;
        }
    }
    return var_ip;
}
