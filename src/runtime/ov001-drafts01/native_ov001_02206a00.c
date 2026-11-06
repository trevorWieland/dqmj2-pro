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
extern u32 native_fn_ov001_022068a0();
extern u32 native_fn_ov001_02206a78();
extern u32 native_fn_ov001_02206aec();
extern u32 native_fn_ov001_02206fb0();
extern u32 native_fn_ov001_02206fdc();
u32 native_ov001_02206a00(void) {
    u32 temp_r0;
    u32 var_r4;
    u32 var_r5;

    temp_r0 = M2C_FIELD((void *) native_fn_ov001_022068a0(), u32 *, 0x74);
    var_r4 = 0;
    var_r5 = 0;
    switch (temp_r0) {
    default:
        break;
    case 0:
        var_r5 = native_fn_ov001_02206a78();
        break;
    case 1:
        var_r5 = native_fn_ov001_02206aec();
        break;
    case 3:
        var_r5 = native_fn_ov001_02206fb0();
        break;
    case 4:
        var_r4 = native_fn_ov001_02206fdc();
        break;
    }
    if (var_r5 == 1) {
        var_r4 = native_ov001_02206a00();
    }
    return var_r4;
}
