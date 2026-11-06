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
extern u32 native_fn_02000c84(void *, u32, u32);
extern u32 native_fn_02000c90(const void *, void *, s32, s32);
extern u32 native_fn_02008cdc(const void *, void *);
extern u32 native_fn_02026144(s32, s32);
u32 native_main_02048778(void *arg0, void *arg1, void *arg2) {
    u32 temp_r4;
    u32 temp_r5;
    u8 sp0[16];

    native_fn_02000c84(&sp0, 0, 0x1000);
    native_fn_02000c90(&sp0, arg0, M2C_FIELD(arg2, u32 *, 0x64), M2C_FIELD(arg2, u32 *, 0x68));
    if (M2C_FIELD(arg2, u32 *, 0x64) != 0) {
        temp_r5 = M2C_FIELD(arg2, u32 *, 0x68);
        if (temp_r5 != 0) {
            temp_r4 = native_fn_02026144(0x01000000, M2C_FIELD(arg2, u32 *, 0x64));
            return native_fn_02000c90(&sp0, arg1, temp_r4, native_fn_02026144(0x01000000, temp_r5));
        }
    }
    return native_fn_02008cdc(&sp0, arg1);
}
