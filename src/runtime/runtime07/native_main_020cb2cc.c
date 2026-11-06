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
extern u32 native_fn_020cb2fc();
extern u32 native_fn_020cbb64();
extern u32 native_fn_020cbbd8();
extern u32 native_fn_020cbc28();
extern u8 native_data_021d6630[];
u32 native_main_020cb2cc(void) {
    if (((s32) (M2C_FIELD(native_data_021d6630, s8 *, 0xD1) << 0x1F) >> 0x1F) != 0) {
        native_fn_020cbb64();
    }
    native_fn_020cb2fc();
    native_fn_020cbbd8();
    return native_fn_020cbc28();
}
