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
extern u32 native_fn_0203cf9c();
extern u32 native_fn_0204122c();
extern u32 native_fn_02041af0();
extern u32 native_fn_02041b80();
u32 native_main_02042c34(u32 arg0) {
    u32 temp_r0;
    u32 var_r5;

    var_r5 = 0;
    if (arg0 < 0x981U) {
        temp_r0 = native_fn_02041af0();
        if ((temp_r0 != 0) && (M2C_FIELD(temp_r0, s32 *, 4) != 0)) {
            if (native_fn_0204122c(temp_r0 + 4) != 0) {
                native_fn_0203cf9c(-1, M2C_FIELD(temp_r0, s32 *, 0xC));
                M2C_FIELD(temp_r0, s32 *, 0xC) = 0;
                native_fn_02041b80(arg0);
                var_r5 = 1;
            }
        }
    }
    return var_r5;
}
