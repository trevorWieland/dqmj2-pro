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
extern u32 native_arm7_fn_037fb8a4(u32);
extern u32 native_arm7_fn_037fb964(u32);
extern u32 native_arm7_fn_037fdef4(u32);
extern u32 native_arm7_fn_037fe6b4(void);
extern u32 native_arm7_fn_037fe410(u32, u32, u32);
extern u32 native_arm7_fn_03807330(void);
extern u16 native_arm7_data_04000208;
u32 native_arm7_wram_037fddf8(void) {
    native_arm7_fn_037fb8a4(0x40000U);
    native_arm7_fn_037fb964(-1U);
    native_arm7_fn_037fdef4(0U);
    native_arm7_fn_037fdef4(1U);
    native_arm7_fn_037fdef4(2U);
    native_arm7_fn_037fdef4(3U);
    native_arm7_fn_037fe6b4();
    do {

    } while (native_arm7_fn_037fe410(0xCU, 0x1000U, 0U) != 0);
    native_arm7_data_04000208 = 0;
    return native_arm7_fn_03807330();
}
