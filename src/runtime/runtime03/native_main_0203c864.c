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
extern u32 native_fn_0203c818();
extern u32 native_fn_0203c830();
u32 native_main_0203c864(s32 arg0, s32 arg1) {
    u32 temp_r0;
    u32 var_r4;

    var_r4 = 0;
    if (native_fn_0203c818() == 0) {
        temp_r0 = native_fn_0203c830();
        if (temp_r0 != 0) {
            M2C_FIELD(temp_r0, s32 *, 4) = arg0;
            M2C_FIELD(temp_r0, s32 *, 8) = arg1;
            var_r4 = 1;
            M2C_FIELD(temp_r0, s32 *, 0) = 1;
        }
    }
    return var_r4;
}
