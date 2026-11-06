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
extern u32 native_fn_02049008();
extern u32 native_fn_0204b138();
extern u32 native_fn_ov001_02202360();
u32 native_ov001_021fe3dc(u32 arg0, s32 arg1) {
    u32 temp_r0;
    u32 temp_r0_2;

    temp_r0 = native_fn_ov001_02202360(arg1);
    if (arg1 == 0) {
        native_fn_02049008(temp_r0, arg0, 0x1B, 0x1A, 0);
    } else {
        native_fn_02049008(temp_r0, arg0, 0x15, 0x16, 0);
    }
    temp_r0_2 = M2C_FIELD(temp_r0, u32 *, 0xA8);
    if (temp_r0_2 == 0x7F) {
        return temp_r0_2;
    }
    if ((s32) M2C_FIELD(temp_r0, s32 *, 4) > 0) {
        native_fn_0204b138(temp_r0 + 0xA8, 0, 1);
    } else {
        native_fn_0204b138(temp_r0 + 0xA8, 0, 0);
    }
    if ((s32) (M2C_FIELD(temp_r0, s32 *, 4) + M2C_FIELD(temp_r0, u16 *, 0xC)) < (s32) M2C_FIELD(temp_r0, u16 *, 0xE)) {
        return native_fn_0204b138(temp_r0 + 0xA8, 1, 1);
    }
    return native_fn_0204b138(temp_r0 + 0xA8, 1, 0);
}
