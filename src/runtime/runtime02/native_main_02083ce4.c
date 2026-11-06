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
extern u32 native_fn_02012824();
extern u32 native_fn_020824b4();
extern u32 native_fn_0208349c();
extern u8 native_data_021c72a0[];
u32 native_main_02083ce4(void) {
    native_fn_020824b4(3);
    if (native_fn_02012824(native_fn_0208349c) != 2) {
        native_fn_020824b4(9);
        return 0U;
    }
    M2C_FIELD(native_data_021c72a0, s16 *, 0xE) = 0;
    return 1U;
}
