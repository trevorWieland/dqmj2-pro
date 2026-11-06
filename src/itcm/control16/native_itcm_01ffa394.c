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
extern u32 native_fn_01ffa824(void);
extern u32 native_fn_020846bc(void);
extern u16 native_data_01fff940;
u32 native_itcm_01ffa394(u32 arg0) {
    u32 var_r0;
    u32 var_r1;

    if (native_fn_01ffa824() & 0xFF) {
        var_r0 = 1;
        if (!(native_data_01fff940 & (1 << arg0))) {
            var_r0 = 0;
        }
        return var_r0;
    }
    return (native_fn_020846bc() & (1 << arg0)) != 0;
}
