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
extern u32 native_arm7_data_038075cc;
u32 native_arm7_wram_037feec4(void) {
    u32 temp_r1;

    temp_r1 = (native_arm7_data_038075cc * 0x19660D) + 0x3C6EF35F;
    native_arm7_data_038075cc = temp_r1;
    return (u32) (u16) (temp_r1 >> 0x10);
}
