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
extern u32 native_fn_0202a498();
extern u32 native_fn_0205fd4c();
extern u8 native_data_021d6bcc[];
u32 native_main_020d1594(void) {
    M2C_FIELD(native_data_021d6bcc, s8 *, 0xD1) = (s8) (M2C_FIELD(native_data_021d6bcc, s8 *, 0xD1) & ~1);
    if (M2C_FIELD(native_data_021d6bcc, s32 *, 0xC8) != 0) {
        native_fn_0202a498(M2C_FIELD(native_data_021d6bcc, s8 *, 0xCC));
    }
    return native_fn_0205fd4c(0, 0);
}
