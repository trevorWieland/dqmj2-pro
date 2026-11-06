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
extern u32 native_fn_02082f44();
extern u8 native_data_021c72a0[];
extern u8 native_data_021c7320[];
extern u8 native_data_021c7400[];
u32 native_main_02082ee4(void) {
    native_fn_020824b4(3);
    if (native_fn_02014008(native_fn_02082f44, M2C_FIELD(native_data_021c72a0, s32 (**)(u8 *, u8 *), 0x40)(native_data_021c7320, native_data_021c7400), native_data_021c7320) == 2) {
        return 1U;
    }
    native_fn_020824c4();
    native_fn_020824b4(9);
    return 0U;
}
