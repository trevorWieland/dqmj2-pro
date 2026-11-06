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
extern u32 native_fn_02013ffc();
extern u32 native_fn_020824c4();
extern u32 native_fn_020829fc();
extern u32 native_fn_02083b94();
extern u8 native_data_021c76c0[];
u32 native_main_020829bc(void) {
    if (native_fn_02013ffc(native_data_021c76c0) != 0) {
        native_fn_020824c4();
        return 0U;
    }
    if (native_fn_020829fc() != 0) {
        return 1U;
    }
    native_fn_02083b94();
    return 0U;
}
