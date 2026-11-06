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
extern u32 native_fn_01ffa02c();
extern u32 native_fn_020840a0();
extern u32 native_fn_020846bc();
u32 native_itcm_01ffa6c0(s32 arg0, s32 arg1) {
    u32 temp_r0;

    if (native_fn_020846bc() & (1 << arg0)) {
        temp_r0 = native_fn_020840a0(arg0);
        if ((temp_r0 == 0) || (M2C_FIELD(temp_r0, u16 *, 2) != arg1) || (M2C_FIELD(temp_r0, u16 *, 0) != *(u16 *) native_fn_01ffa02c())) {
            return 0U;
        }
        return temp_r0 + 4;
    }
    return 0U;
}
