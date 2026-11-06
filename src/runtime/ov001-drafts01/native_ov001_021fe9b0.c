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
extern u32 native_fn_ov001_021fc8f0();
extern u32 native_fn_ov001_021fdbcc();
extern u32 native_fn_ov001_021fdd74();
extern u32 native_fn_ov001_021fe54c();
extern u32 native_fn_ov001_022023c4();
extern u32 native_fn_ov001_02204d24();
u32 native_ov001_021fe9b0(void) {
    native_fn_ov001_021fe54c(8, 0x18);
    native_fn_ov001_021fe54c(8, 0x1F);
    native_fn_ov001_021fe54c(0, 0x7F);
    native_fn_ov001_021fe54c(0, 0x1E);
    native_fn_ov001_021fe54c(0, 0x15);
    native_fn_ov001_021fe54c(0, 0x16);
    native_fn_ov001_021fe54c(0, 0x1B);
    native_fn_ov001_021fe54c(0, 0x1A);
    native_fn_ov001_021fe54c(0, 0x20);
    native_fn_ov001_021fe54c(0, 0x21);
    native_fn_ov001_02204d24(0);
    native_fn_ov001_02204d24(2);
    native_fn_ov001_021fc8f0();
    native_fn_ov001_021fdd74();
    native_fn_ov001_021fdbcc();
    return native_fn_ov001_022023c4(2);
}
