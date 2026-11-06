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
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_02062aa0();
extern u32 native_fn_ov000_021f79e0();
u32 native_ov000_021f776c(void) {
    s32 temp_r0_2;
    s32 var_r5;
    u32 temp_r0;

    temp_r0_2 = (s32) native_fn_02062aa0();
    var_r5 = 0;
    if (temp_r0_2 <= 0) {
        return (u32) temp_r0_2;
    }
    do {
        native_fn_ov000_021f79e0((s8) (var_r5 + 7));
        temp_r0 = native_fn_ov000_021f79e0((s8) (var_r5 + 0xA));
        var_r5 += 1;
    } while (var_r5 < temp_r0_2);
    return temp_r0;
}
