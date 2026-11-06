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
extern u32 native_fn_02014008();
extern u32 native_fn_020824b4();
extern u32 native_fn_020824c4();
extern u32 native_fn_020825e4();
extern u8 native_data_021c72a0[];
extern u8 native_data_021c7320[];
extern u8 native_data_021c7360[];
u32 native_main_02082584(void) {
    native_fn_020824b4(3);
    if (native_fn_02014008(native_fn_020825e4, M2C_FIELD(native_data_021c72a0, s32 (**)(u8 *, u8 *), 0x38)(native_data_021c7320, native_data_021c7360), native_data_021c7320) == 2) {
        return 1U;
    }
    native_fn_020824c4();
    native_fn_020824b4(9);
    return 0U;
}
