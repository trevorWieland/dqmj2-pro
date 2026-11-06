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
extern u32 native_fn_02049ad0();
extern u32 native_fn_02085418();
extern u32 native_fn_ov001_0220aba0();
extern u32 native_fn_ov001_0220ac58();
u32 native_ov001_0220af68(void *arg0) {
    native_fn_ov001_0220aba0(1, M2C_FIELD(arg0, s8 *, 0x10), 3, 0x16, 1, 0xA, 2, 0, 1);
    native_fn_ov001_0220ac58(1, 5, 4, 4, 8);
    return native_fn_02085418(M2C_FIELD(*(void **) native_fn_02049ad0(1), s32 *, 4), 3);
}
