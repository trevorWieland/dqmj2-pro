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
extern u32 native_fn_02046384();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_02085270();
extern u32 native_fn_02085284();
extern u32 native_fn_02086948();
extern u32 native_fn_02086b14();
extern u32 native_fn_02086b68();
u32 native_main_0208632c(void *arg0) {
    M2C_FIELD(arg0, s32 *, 0x24) = (s32) *M2C_FIELD(arg0, s32 **, 0x20);
    native_fn_02046384(M2C_FIELD(arg0, u8 *, 0x2E), M2C_FIELD(arg0, u8 *, 0x1C), M2C_FIELD(arg0, u8 *, 0x1D), M2C_FIELD(arg0, u8 *, 0x1E), (s32) M2C_FIELD(arg0, u8 *, 0x1F), 0, (s32) M2C_FIELD(arg0, u8 *, 0x3A));
    native_fn_02085284(arg0 + 0x3C, 0, 2, (u16) M2C_FIELD(arg0, s32 *, 0x94));
    native_fn_02086948(arg0, 1);
    native_fn_02085270(arg0 + 0x3C, 0x18, 8);
    native_fn_02086b68(arg0, M2C_FIELD(arg0, s32 *, 0x64), M2C_FIELD(arg0, u16 *, 0x6C));
    native_fn_0205e7a8(-1, 0x57);
    native_fn_02086b14(arg0, 0x13);
    return 1U;
}
