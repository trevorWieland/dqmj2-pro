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
extern u32 native_fn_02062074();
extern u32 native_fn_020620a0();
extern u32 native_fn_ov000_02215698();
extern u32 native_fn_ov000_022156d4();
u32 native_main_020766dc(void) {
    u32 temp_r0;

    native_fn_ov000_02215698();
    native_fn_ov000_022156d4();
    temp_r0 = native_fn_020620a0();
    if (temp_r0 == 0) {
        return temp_r0;
    }
    return native_fn_02062074(0);
}
