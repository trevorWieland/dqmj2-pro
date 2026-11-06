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
extern u32 native_fn_ov000_0221c658();
extern u32 native_fn_ov000_0221c758();
extern u32 native_fn_ov000_0221c938();
u32 native_ov000_0221cb8c(void) {
    native_fn_ov000_0221c758(0x1F, M2C_FIELD((void *) native_fn_ov000_0221c658(), s8 *, 0x10), 3, 0x13, 3, 0xD, 2, 1, 1);
    native_fn_ov000_0221c938(0x1F, 5, 2, 3, 0x10);
    return native_fn_02085418(M2C_FIELD(*(void **) native_fn_02049ad0(0x1F), s32 *, 4), 3);
}
