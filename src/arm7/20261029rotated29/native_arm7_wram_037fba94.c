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
#define NULL ((void *)0)
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_arm7_fn_037fdd2c(void);
extern u32 native_arm7_fn_037fdd00(void);
extern u32 native_arm7_fn_037fe2ac(u32, u32);
extern u32 native_arm7_fn_037fdd40(u32);
extern u32 native_arm7_fn_037fdd14(u32);
u32 native_arm7_wram_037fba94(u32 arg0, u32 arg1, s32 (*arg2)(), s32 arg3) {
    u32 temp_r0;
    u32 var_r0;

    if (arg3 != 0) {
        var_r0 = native_arm7_fn_037fdd2c();
    } else {
        var_r0 = native_arm7_fn_037fdd00();
    }
    temp_r0 = native_arm7_fn_037fe2ac(arg0, arg1);
    if (temp_r0 == 0) {
        if (arg2 != NULL) {
            arg2();
        }
        M2C_FIELD(arg1, s16 *, 4) = (s16) arg0;
    }
    if (arg3 != 0) {
        native_arm7_fn_037fdd40(var_r0);
    } else {
        native_arm7_fn_037fdd14(var_r0);
    }
    return temp_r0;
}
