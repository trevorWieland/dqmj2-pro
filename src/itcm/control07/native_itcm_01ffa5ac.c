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
extern u32 native_fn_01ffb810(s32, s32, s16);
extern u32 native_fn_02008e0c();
extern u32 native_data_021cebe0;
u32 native_itcm_01ffa5ac(s32 arg0, s32 arg1, s16 arg2) {
    void *temp_r0;

    if (M2C_FIELD(&native_data_021cebe0, s32 *, 0x30) == 1) {
        return native_fn_01ffb810(arg0, arg1, arg2);
    }
    native_fn_02008e0c(arg0, native_fn_01ffa02c() + 4, arg1);
    temp_r0 = (void *) native_fn_01ffa02c();
    M2C_FIELD(temp_r0, s16 *, 2) = arg2;
    return (u32) temp_r0;
}
