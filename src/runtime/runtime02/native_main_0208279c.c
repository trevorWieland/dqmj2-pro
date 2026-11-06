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
extern u32 native_fn_02013080();
extern u32 native_fn_020824b4();
extern u32 native_fn_020824c4();
extern u32 native_fn_02082824();
extern u8 native_data_021c72a0[];
u32 native_main_0208279c(void) {
    if ((u32) (M2C_FIELD(native_data_021c72a0, s32 *, 0x34) - 4) <= 2U) {
        return 1U;
    }
    native_fn_020824b4(4);
    if (native_fn_02013080(native_fn_02082824, M2C_FIELD(native_data_021c72a0, s32 *, 0x20), (u16) M2C_FIELD(native_data_021c72a0, s32 *, 0x54), M2C_FIELD(native_data_021c72a0, s32 *, 0x3C), (s32) (u16) M2C_FIELD(native_data_021c72a0, s32 *, 0x58), 1) == 2) {
        return 1U;
    }
    native_fn_020824c4();
    return 0U;
}
