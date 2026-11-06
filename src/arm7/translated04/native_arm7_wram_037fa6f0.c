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
extern u32 native_arm7_fn_027eb850(u32);
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_wram_037fa6f0(void) {
    s32 temp_r5;
    u32 temp_r4;

    temp_r5 = native_arm7_data_0380fff4 + 0x42C;
    temp_r4 = native_arm7_fn_027eb850(temp_r5 + 0x50);
    return temp_r4 | native_arm7_fn_027eb850(temp_r5 + 0x64);
}
