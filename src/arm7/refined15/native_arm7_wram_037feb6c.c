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
extern u32 native_arm7_data_038075c8;
extern u8 native_arm7_data_03807984;
u32 native_arm7_wram_037feb6c(u32 arg0) {
    s32 var_r2;
    s32 var_r3;
    u8 temp_r1;
    void *temp_r0;
    void *temp_r0_2;

    native_arm7_data_038075c8 = arg0;
    if ((s32) arg0 >= 0) {
        var_r2 = 0;
        do {
            temp_r0_2 = (var_r2 * 0x10) + 0x04000000;
            var_r2 += 1;
            M2C_FIELD(temp_r0_2, u8 *, 0x402) = (u8) arg0;
        } while (var_r2 < 0x10);
        return (u32) temp_r0_2;
    }
    var_r3 = 0;
    do {
        temp_r1 = *(&native_arm7_data_03807984 + var_r3);
        temp_r0 = (var_r3 * 0x10) + 0x04000000;
        var_r3 += 1;
        M2C_FIELD(temp_r0, u8 *, 0x402) = temp_r1;
    } while (var_r3 < 0x10);
    return (u32) temp_r0;
}
