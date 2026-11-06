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
extern u32 native_fn_020491f8();
extern u32 native_fn_02049604();
extern u32 native_fn_ov000_021e7b9c();
u32 native_ov000_0221794c(void *arg0) {
    s32 temp_r4;
    u32 temp_r5;

    temp_r4 = M2C_FIELD(arg0, s32 *, 4);
    temp_r5 = native_fn_020491f8();
    if (temp_r4 != M2C_FIELD(arg0, s32 *, 4)) {
        native_fn_02049604(arg0, 1);
        native_fn_ov000_021e7b9c(0x56);
    } else if (temp_r5 != 0) {
        native_fn_ov000_021e7b9c(0x55);
    }
    return temp_r5;
}
