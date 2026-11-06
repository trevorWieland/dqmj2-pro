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
extern u32 native_arm7_fn_037fbe90(void);
extern u32 native_arm7_fn_037fdd14(u32);
u32 native_arm7_wram_037fc36c(void *arg0) {
    u32 temp_r4;

    temp_r4 = native_arm7_fn_037fdd00();
    M2C_FIELD(arg0, s32 *, 0x48) = 1;
    native_arm7_fn_037fbe90();
    return native_arm7_fn_037fdd14(temp_r4);
}
