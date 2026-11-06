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
extern u32 native_fn_02083e28();
extern u32 native_fn_020846bc();
extern u8 native_data_021c9600[];
u32 native_main_020840a0(u32 arg0) {
    u32 var_r4;

    var_r4 = 0;
    if ((arg0 < (u32) (native_fn_02083e28() + 1)) && (native_fn_020846bc() & (1 << arg0))) {
        var_r4 = (arg0 * M2C_FIELD(native_data_021c9600, u16 *, 8)) + M2C_FIELD(native_data_021c9600, s32 *, 0xC);
    }
    return var_r4;
}
