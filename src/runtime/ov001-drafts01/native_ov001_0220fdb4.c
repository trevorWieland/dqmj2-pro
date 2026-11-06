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
extern u32 native_fn_ov001_021d908c();
extern u32 native_fn_ov001_021dcda8();
extern u32 native_fn_ov001_02209490();
extern u32 native_fn_ov001_0220e910();
extern u32 native_fn_ov001_02210ad0();
u32 native_ov001_0220fdb4(void *arg0, void *arg1, s32 arg2) {
    u32 temp_r4;
    u32 temp_r5;

    temp_r5 = native_fn_ov001_0220e910(M2C_FIELD(arg1, u8 *, 0x31E), 0xC, 9);
    if (native_fn_ov001_021dcda8(arg1) != 0) {
        return 0U;
    }
    temp_r4 = native_fn_ov001_02209490(arg1 + 0x22C);
    if (((s32) native_fn_0207b674(0x45, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) && (arg2 == 0) && (native_fn_ov001_02210ad0(arg0, 0x64, native_fn_ov001_021d908c(temp_r5, M2C_FIELD(M2C_FIELD(arg1, void **, 0x1E8), u8 *, 0x8F), temp_r4)) != 0)) {
        return 1U;
    }
    return 0U;
}
