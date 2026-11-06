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
extern u32 native_fn_0200235c();
extern u32 native_fn_020028d8();
extern u32 native_fn_02041f90();
u32 native_main_020424f4(void *arg0) {
    if (((s32) *M2C_FIELD(arg0, s32 **, 0x60) >> 0xC) != 0) {
        return 0U;
    }
    native_fn_02041f90(arg0, native_fn_0200235c(native_fn_020028d8(M2C_FIELD(arg0, s32 *, 0x178) - M2C_FIELD(arg0, s32 *, 0x70), M2C_FIELD(arg0, s32 *, 0x180) - M2C_FIELD(arg0, s32 *, 0x78)), 0x47), 1);
    return 1U;
}
