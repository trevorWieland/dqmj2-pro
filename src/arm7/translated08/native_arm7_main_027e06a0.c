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
extern u32 native_arm7_fn_037fdd00(void);
extern u32 native_arm7_fn_037fc558(void);
extern u32 native_arm7_fn_037fc3c0(u32, u32);
extern u32 native_arm7_fn_027e8bbc(void);
extern u32 native_arm7_fn_037fc590(void);
extern u32 native_arm7_fn_037fdd14(u32);
extern u32 native_arm7_data_027f8884;
extern u32 native_arm7_data_0380b3c0;
extern u32 native_arm7_data_0380b31c;
u32 native_arm7_main_027e06a0(void) {
    u32 temp_r4;

    temp_r4 = native_arm7_fn_037fdd00();
    native_arm7_fn_037fc558();
    native_arm7_fn_037fc3c0((u32) &native_arm7_data_0380b3c0, M2C_FIELD(&native_arm7_data_027f8884, u32 *, 0x578));
    native_arm7_fn_037fc3c0(native_arm7_fn_027e8bbc(), M2C_FIELD(&native_arm7_data_027f8884, u32 *, 0x57C));
    native_arm7_fn_037fc3c0((u32) &native_arm7_data_0380b31c, M2C_FIELD(&native_arm7_data_027f8884, u32 *, 0x580));
    native_arm7_fn_037fc590();
    return native_arm7_fn_037fdd14(temp_r4);
}
