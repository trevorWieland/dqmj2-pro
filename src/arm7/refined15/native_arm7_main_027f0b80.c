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
extern u32 native_arm7_fn_037fb928(u32);
extern u32 native_arm7_fn_037facb4(void);
extern u32 native_arm7_fn_037fb8f0(u32);
extern u32 native_arm7_data_0380fff4;
extern u16 native_arm7_data_048080b4;
u32 native_arm7_main_027f0b80(void) {
    u32 temp_r0;
    void *temp_r4;

    temp_r4 = native_arm7_data_0380fff4 + 0x42C;
    temp_r0 = native_arm7_fn_037fb928(0x01000000U);
    native_arm7_data_048080b4 = 2;
    if (M2C_FIELD(temp_r4, u16 *, 0x3C) != 0) {
        native_arm7_fn_037facb4();
    }
    return native_arm7_fn_037fb8f0(temp_r0);
}
