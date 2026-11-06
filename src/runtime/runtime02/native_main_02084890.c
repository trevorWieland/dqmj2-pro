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
extern u32 native_fn_020848d4();
extern u32 native_fn_02087e84();
extern u8 native_data_020de6b4[];
extern u8 native_data_020de6c4[];
u32 native_main_02084890(void) {
    native_fn_020848d4(0);
    native_fn_020848d4(1);
    native_fn_020848d4(2);
    native_fn_02087e84(native_data_020de6b4, 0);
    return native_fn_02087e84(native_data_020de6c4, 1);
}
