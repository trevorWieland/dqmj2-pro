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
extern u8 native_data_020e2cf4[] __attribute__((aligned(2)));
u32 native_main_020c1fa4(void) {
    void *temp_r0;
    s32 var_ip;

    var_ip = 0;
    do {
        *(native_data_020e2cf4 + (var_ip * 4)) = 0x64;
        temp_r0 = native_data_020e2cf4 + (var_ip * 4);
        M2C_FIELD(temp_r0, s8 *, 1) = 0;
        M2C_FIELD(temp_r0, s8 *, 2) = 0;
        var_ip += 1;
        M2C_FIELD(temp_r0, s8 *, 3) = 0;
    } while (var_ip < 0x10);
    return (u32) temp_r0;
}
