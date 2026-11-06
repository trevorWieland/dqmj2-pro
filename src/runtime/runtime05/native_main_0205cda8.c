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
u32 native_main_0205cda8(u32 arg0, s32 arg1, s32 arg2, s32 arg3) {
    s32 temp_ip;
    u32 var_r4;
    void *temp_ip_2;

    var_r4 = 0;
    if (arg0 < 0x20U) {
        temp_ip = arg0 * 0x11C;
        temp_ip_2 = native_data_021043ac + temp_ip;
        if (*(native_data_021043ac + temp_ip) == 3) {
            M2C_FIELD(temp_ip_2, s32 *, 0x84) = arg1;
            M2C_FIELD(temp_ip_2, s32 *, 0x88) = arg2;
            M2C_FIELD(temp_ip_2, s32 *, 0x8C) = arg3;
            var_r4 = 1;
        }
    }
    return var_r4;
}
