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
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
extern u32 native_fn_02008d78();
extern u32 native_fn_02063ed4();
extern u32 native_fn_02063eec();
extern u32 native_fn_02067748();
extern u32 native_fn_02067a40();
extern u32 native_fn_020684ac();
u32 native_main_02068520(void) {
    s32 *temp_r0;
    s32 temp_r4;

    temp_r4 = *(s32 *) native_fn_02063ed4();
    native_fn_02008d78(native_fn_02063eec(), 0, 0x100);
    native_fn_02008d78(native_fn_02067a40(), 0, 0xC);
    native_fn_02008d78(native_fn_02067748(), 0, 0x38);
    if (temp_r4 != 0) {
        *(s32 *) native_fn_02063ed4() = 0;
        return native_fn_020684ac(3, 1);
    }
    temp_r0 = (s32 *) native_fn_02063ed4();
    *temp_r0 = 0;
    return (u32) temp_r0;
}
