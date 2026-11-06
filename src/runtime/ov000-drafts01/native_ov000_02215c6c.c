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
extern u32 native_fn_02062a10();
extern u32 native_fn_0207b1c4();
extern u32 native_fn_0207b460();
extern u8 native_data_ov000_0224575c[];
u32 native_ov000_02215c6c(s32 arg0, u32 arg1) {
    s32 temp_r5;
    void *temp_r0;

    temp_r5 = (arg0 * 0x64) + (s32) native_data_ov000_0224575c;
    temp_r0 = (void *) native_fn_02062a10(arg1);
    native_fn_0207b460(M2C_FIELD(temp_r0, s16 *, 0x18), M2C_FIELD(temp_r0, u8 *, 0x1A), temp_r0 + 0x7A, temp_r5 + 0x20);
    return native_fn_0207b1c4(temp_r0 + 0x7A, temp_r5 + 0x20, temp_r5);
}
