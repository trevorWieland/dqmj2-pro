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
extern u32 native_arm7_data_03807edc;
u32 native_arm7_wram_03801c70(s32 arg0, s16 arg1) {
    void *temp_r0;

    temp_r0 = native_arm7_data_03807edc + (arg0 * 2);
    M2C_FIELD(temp_r0, s16 *, 0x260) = arg1;
    return temp_r0 + 0x200;
}
