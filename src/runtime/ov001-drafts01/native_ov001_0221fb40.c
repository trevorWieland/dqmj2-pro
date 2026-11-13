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
extern u32 ov001_mode_byte_021db530();
extern u32 native_fn_ov001_021db578();
u32 native_ov001_0221fb40(void **arg0) {
    u32 temp_r4_2;
    u32 temp_r5;
    u32 temp_r6;
    u8 temp_r4;
    u8 var_r7;

    temp_r4 = M2C_FIELD(*arg0, u8 *, 0x31E);
    if (temp_r4 == 0) {
        var_r7 = 2;
    } else {
        var_r7 = 3;
    }
    temp_r6 = ov001_mode_byte_021db530(temp_r4);
    temp_r5 = ov001_mode_byte_021db530(var_r7);
    temp_r4_2 = native_fn_ov001_021db578(temp_r4);
    if ((s32) (temp_r6 + temp_r5) >= (s32) (temp_r4_2 + native_fn_ov001_021db578(var_r7) + 2)) {
        return 1U;
    }
    return 0U;
}
