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
extern u32 native_fn_02049ffc();
extern u32 native_fn_ov000_0221571c();
extern u32 native_fn_ov000_022167dc();
extern u32 native_fn_ov000_02217a78();
u32 native_ov000_02217ac8(s32 arg0) {
    void **temp_r0;

    native_fn_ov000_0221571c();
    if (arg0 != 0) {
        return native_fn_ov000_02217a78();
    }
    temp_r0 = (void **) native_fn_02049ad0(0x1F);
    native_fn_02049ffc(M2C_FIELD(*temp_r0, s32 *, 4));
    return native_fn_ov000_022167dc(temp_r0);
}
