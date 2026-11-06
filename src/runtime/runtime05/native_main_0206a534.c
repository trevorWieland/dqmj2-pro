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
extern u8 native_data_021c4a04[];
u32 native_main_0206a534(s32 arg0, u8 *arg1, u8 *arg2, u8 *arg3) {
    u8 temp_r0;
    void *temp_ip;

    temp_ip = native_data_021c4a04 + (arg0 * 0x10);
    *arg1 = M2C_FIELD(temp_ip, u8 *, 8);
    *arg2 = M2C_FIELD(temp_ip, u8 *, 6);
    temp_r0 = M2C_FIELD(temp_ip, u8 *, 7);
    *arg3 = temp_r0;
    return (u32) temp_r0;
}
