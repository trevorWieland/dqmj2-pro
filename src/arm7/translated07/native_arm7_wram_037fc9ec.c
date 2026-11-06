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
extern u32 native_arm7_fn_037fca1c(void);
extern u32 native_arm7_fn_037fe2b4(void);
extern u32 native_arm7_fn_037fb998(void);
extern u32 native_arm7_fn_037fb798(void);
extern u32 native_arm7_fn_037fd128(void);
extern u32 native_arm7_fn_037fd34c(void);
extern u32 native_arm7_fn_037fbf64(void);
extern u32 native_arm7_fn_037fdd7c(void);
extern u32 native_arm7_fn_038063f8(void);
u32 native_arm7_wram_037fc9ec(void) {
    native_arm7_fn_037fca1c();
    native_arm7_fn_037fe2b4();
    native_arm7_fn_037fb998();
    native_arm7_fn_037fb798();
    native_arm7_fn_037fd128();
    native_arm7_fn_037fd34c();
    native_arm7_fn_037fbf64();
    native_arm7_fn_037fdd7c();
    return native_arm7_fn_038063f8();
}
