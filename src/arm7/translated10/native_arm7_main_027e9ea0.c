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
extern u32 native_arm7_data_0380fff4;
extern u32 native_arm7_data_04808038;
u32 native_arm7_main_027e9ea0(void) {
    u16 temp_r0;

    M2C_FIELD(native_arm7_data_0380fff4, s16 *, 0x3EA) = 1;
    temp_r0 = M2C_FIELD(native_arm7_data_0380fff4, u16 *, 0x468);
    if (temp_r0 != 0) {
        return (u32) temp_r0;
    }
    M2C_FIELD((u32) &native_arm7_data_04808038, u16 *, 0) = (u16) (M2C_FIELD((u32) &native_arm7_data_04808038, u16 *, 0) & ~2);
    M2C_FIELD((u32) &native_arm7_data_04808038, s16 *, 0x10) = 0;
    return 0U;
}
