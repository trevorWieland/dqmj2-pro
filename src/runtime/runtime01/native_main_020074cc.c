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
extern u32 native_fn_02006de4();
extern u32 native_fn_02007560();
extern u32 native_fn_02007644();
extern u32 native_fn_020076ec();
extern u32 native_fn_02007700();
extern u32 native_fn_0200775c();
extern u32 native_fn_02007764();
extern u8 native_data_020e363c[];
u32 native_main_020074cc(void) {
    u32 temp_r0;

    native_fn_020076ec(2, native_fn_02007560(2));
    native_fn_02007700(2, native_fn_02007644(2));
    if (M2C_FIELD(native_data_020e363c, s32 *, 4) != 0) {
        temp_r0 = native_fn_02006de4() & 3;
        if (temp_r0 != 1) {
            return temp_r0;
        }
    }
    native_fn_0200775c(0x0200002B);
    return native_fn_02007764(0x023E0021);
}
