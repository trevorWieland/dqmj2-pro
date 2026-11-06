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
extern u32 native_fn_ov001_02207938();
extern u32 native_fn_ov001_02208460();
extern u32 native_fn_ov001_02208594();
extern u32 native_fn_ov001_022086b4();
extern u32 native_fn_ov001_02208d40();
extern u32 native_fn_ov001_02208e70();
u32 native_ov001_02208408(s32 arg0) {
    u32 temp_r0;
    u32 temp_r0_2;

    temp_r0_2 = native_fn_ov001_02207938();
    if (arg0 == 3) {
        return temp_r0_2;
    }
    native_fn_ov001_02208460(M2C_FIELD(temp_r0_2, s32 *, 0x24));
    temp_r0 = native_fn_ov001_02208594(arg0);
    switch (arg0) {
    default:
        return temp_r0;
    case 0:
        return native_fn_ov001_022086b4();
    case 1:
        return native_fn_ov001_02208d40();
    case 2:
        return native_fn_ov001_02208e70();
    }
}
