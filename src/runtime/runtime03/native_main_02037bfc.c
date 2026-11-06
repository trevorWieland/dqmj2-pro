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
extern u32 native_fn_0202b7e4();
extern u32 native_fn_0202b834();
extern u32 native_fn_02037d6c();
u32 native_main_02037bfc(void *arg0) {
    if (native_fn_0202b7e4(M2C_FIELD(arg0, s32 *, 0), M2C_FIELD(arg0, u16 *, 0xC)) == 0) {
        return -1U;
    }
    if (native_fn_02037d6c(arg0) != 0) {
        return M2C_FIELD(arg0, u16 *, 0xC) - 1;
    }
    native_fn_0202b834(M2C_FIELD(arg0, s32 *, 0), 0);
    return -1U;
}
