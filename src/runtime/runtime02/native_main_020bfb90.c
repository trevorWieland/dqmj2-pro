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
extern u32 native_fn_0205fd0c();
extern u32 native_fn_0205fd34();
extern u32 native_fn_0205fd40();
extern u32 native_fn_0205fd70();
extern u32 native_fn_02062378();
extern u32 native_fn_02071b9c();
extern u8 native_data_021d4bec[];
u32 native_main_020bfb90(void) {
    if (native_fn_0205fd70() != 0) {
        if (native_fn_02062378() == 6) {
            native_fn_02071b9c();
        }
        native_fn_0205fd34(native_fn_0205fd70(), 0x10);
        if (native_fn_0205fd70() != 0) {
            do {
                if (native_fn_02062378() != 6) {
                    native_fn_0205fd40();
                } else {
                    native_fn_0205fd70();
                    native_fn_0205fd0c();
                }
            } while (native_fn_0205fd70() != 0);
        }
    }
    M2C_FIELD(native_data_021d4bec, s8 *, 1) = 1;
    return (u32) native_data_021d4bec;
}
