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
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
extern u32 native_fn_02008d78();
extern u32 native_fn_02008e0c();
extern u32 native_fn_0207f3b0();
extern u32 native_fn_020cf27c();
u32 native_main_020cf0fc(void) {
    u32 temp_r0;

    temp_r0 = native_fn_020cf27c();
    native_fn_02008d78(temp_r0, 0, 0x18);
    return native_fn_02008e0c(native_fn_0207f3b0(), temp_r0, 0x18);
}
