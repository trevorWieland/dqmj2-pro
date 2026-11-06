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
extern u32 native_fn_0206d230();
extern u32 native_fn_ov001_021fc63c();
extern u32 native_fn_ov001_021fdc8c();
extern u32 native_fn_ov001_022023c4();
extern u32 native_fn_ov001_02202e30();
extern u32 native_fn_ov001_02202e98();
extern u32 native_fn_ov001_02202f24();
u32 native_ov001_02202e08(void) {
    native_fn_0206d230();
    native_fn_ov001_021fdc8c();
    native_fn_ov001_021fc63c();
    native_fn_ov001_02202e98();
    native_fn_ov001_02202f24();
    native_fn_ov001_02202e30();
    return native_fn_ov001_022023c4(0x86);
}
