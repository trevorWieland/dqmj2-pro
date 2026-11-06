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
extern u32 native_fn_0208ebbc();
u32 native_main_0208ebd8(s32 arg0, void *arg1, s8 arg2) {
    u32 temp_r0;

    temp_r0 = native_fn_0208ebbc(arg2);
    if (temp_r0 != 0) {
        M2C_FIELD(temp_r0, s32 *, 0) = arg0;
        M2C_FIELD(temp_r0, void **, 4) = arg1;
        M2C_FIELD(temp_r0, s32 *, 8) = 0;
        M2C_FIELD(temp_r0, s8 *, 0xC) = (s8) M2C_FIELD(arg1, s8 *, 0x73);
        M2C_FIELD(temp_r0, s8 *, 0xD) = arg2;
    }
    return temp_r0;
}
