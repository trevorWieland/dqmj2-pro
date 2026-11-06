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
extern u32 native_fn_0207b674();
extern u32 native_fn_ov001_021dbd24();
extern u32 native_fn_ov001_021e29e8();
extern u32 native_fn_ov001_02210ad0();
u32 native_ov001_0220f530(void *arg0, s32 arg1) {
    if ((arg1 != 0) && ((s32) native_fn_0207b674(0x2F, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) && ((s32) native_fn_ov001_021dbd24(arg0) <= 0) && (native_fn_ov001_02210ad0(arg0, 0xA, 3) != 0) && !(native_fn_ov001_021e29e8() & 0x20)) {
        M2C_FIELD(arg0, s16 *, 0x1F0) = 1;
        M2C_FIELD(arg0, u32 *, 0x33C) = (u32) (M2C_FIELD(arg0, u32 *, 0x33C) | 2);
    }
    if (((s32) native_fn_0207b674(0x25, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) && ((s32) native_fn_ov001_021dbd24(arg0) <= 0) && (native_fn_ov001_02210ad0(arg0, 0x64, 0xA) != 0) && !(native_fn_ov001_021e29e8() & 0x20)) {
        M2C_FIELD(arg0, u32 *, 0x33C) = (u32) (M2C_FIELD(arg0, u32 *, 0x33C) | 4);
    }
    return M2C_FIELD(arg0, u32 *, 0x33C);
}
