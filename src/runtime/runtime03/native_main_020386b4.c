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
extern u32 native_fn_0202bac4();
extern u32 native_fn_0202bb88();
extern u8 native_data_020f436c[];
u32 native_main_020386b4(void *arg0) {
    u32 var_r1;

    var_r1 = native_fn_0202bb88(native_data_020f436c, 0);
    if (var_r1 != 0) {
loop_2:
        if ((u32) M2C_FIELD(arg0, u8 *, 0x3D) >= (u32) M2C_FIELD(var_r1, u8 *, 0x3D)) {
            var_r1 = native_fn_0202bb88(native_data_020f436c);
            if (var_r1 != 0) {
                goto loop_2;
            }
        }
    }
    return native_fn_0202bac4(native_data_020f436c, var_r1, arg0);
}
