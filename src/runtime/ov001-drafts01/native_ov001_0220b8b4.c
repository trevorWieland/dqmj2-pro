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
extern u32 native_fn_ov001_021d75d4();
extern u32 native_fn_ov001_021d77b0();
extern u32 native_fn_ov001_021d7814();
extern u32 native_fn_ov001_021d94cc();
extern u32 native_fn_ov001_021e33f0();
extern u32 native_fn_ov001_021e3424();
extern u32 native_fn_ov001_021e34f0();
u32 native_ov001_0220b8b4(void) {
    native_fn_ov001_021d75d4(0x2D);
    native_fn_ov001_021d94cc(0, 0);
    native_fn_ov001_021d77b0(-1, native_fn_ov001_021e3424());
    native_fn_ov001_021d7814(-1, native_fn_ov001_021e33f0(0));
    return native_fn_ov001_021e34f0(1);
}
