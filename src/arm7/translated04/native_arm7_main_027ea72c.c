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
extern u32 native_arm7_data_027f735c;
u32 native_arm7_main_027ea72c(void) {
    u32 *temp_r1;
    u32 var_r3;
    void *temp_r0;

    var_r3 = 0;
    do {
        temp_r1 = &(&native_arm7_data_027f735c)[var_r3];
        temp_r0 = M2C_FIELD(&(&native_arm7_data_027f735c)[var_r3], u16 *, 0) + 0x04800000;
        var_r3 += 1;
        M2C_FIELD(temp_r0, u16 *, 0x8000) = (u16) M2C_FIELD(temp_r1, u16 *, 2);
    } while (var_r3 < 0x19U);
    return temp_r0 + 0x8000;
}
