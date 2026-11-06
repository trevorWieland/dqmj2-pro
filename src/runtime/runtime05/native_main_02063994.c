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
extern u8 native_data_021bd51c[];
extern u8 native_data_021c0c64[];
u32 native_main_02063994(s32 arg0) {
    s32 temp_lr;
    u8 temp_r2;
    u8 var_r0;
    u8 var_r3;
    void *temp_ip;

    temp_lr = arg0 * 0xC;
    var_r0 = 0;
    var_r3 = 0;
    temp_ip = native_data_021bd51c + temp_lr;
    do {
        temp_r2 = M2C_FIELD((temp_ip + var_r3), u8 *, 0x3748);
        if (temp_r2 != 0) {
            M2C_FIELD((temp_ip + var_r0), u8 *, 0x3748) = temp_r2;
            var_r0 += 1;
        }
        var_r3 += 1;
    } while ((u32) var_r3 < 0xAU);
    if ((u32) var_r0 >= 0xAU) {
        return (u32) var_r0;
    }
    *(var_r0 + (native_data_021c0c64 + temp_lr)) = 0;
    return (u32) var_r0;
}
