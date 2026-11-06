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
extern u32 native_fn_02044424();
extern u32 native_fn_0207b004();
u32 native_ov001_021e13c8(void *arg0, u32 arg1) {
    u32 var_r4;

    var_r4 = 0;
    if ((native_fn_02044424(0x1000) != 0) && (M2C_FIELD(arg0, u8 *, 0x31E) == 0) && (native_fn_0207b004(arg1, 0x40) != 0)) {
        var_r4 = 1;
    }
    return var_r4;
}
