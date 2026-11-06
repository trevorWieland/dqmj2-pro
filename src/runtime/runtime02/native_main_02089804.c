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
u32 native_main_02089804(void) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;

    temp_r0_3 = native_fn_0205fd70();
    if (temp_r0_3 == 0) {
        return temp_r0_3;
    }
    if (native_fn_02062378() == 6) {
        native_fn_02071b9c();
    }
    native_fn_0205fd34(native_fn_0205fd70(), 0x10);
    temp_r0_2 = native_fn_0205fd70();
    if (temp_r0_2 == 0) {
        return temp_r0_2;
    }
    do {
        if (native_fn_02062378() != 6) {
            native_fn_0205fd40();
        } else {
            native_fn_0205fd70();
            native_fn_0205fd0c();
        }
        temp_r0 = native_fn_0205fd70();
    } while (temp_r0 != 0);
    return temp_r0;
}
