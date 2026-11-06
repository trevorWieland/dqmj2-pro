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
extern u32 native_fn_ov001_02204244();
extern u32 native_fn_ov001_02204250();
extern u32 native_fn_ov001_02204270();
u32 native_ov001_02204aa0(void *arg0, s32 arg1) {
    u32 temp_r0;
    u32 temp_r6;

    temp_r0 = native_fn_ov001_02204270();
    if (temp_r0 == 0x7F) {
        return temp_r0;
    }
    temp_r6 = native_fn_ov001_02204250();
    native_fn_ov001_02204244();
    M2C_FIELD(temp_r6, s32 *, 0) = 6;
    M2C_FIELD(temp_r6, s8 *, 0x24) = 0;
    M2C_FIELD(temp_r6, s16 *, 0x14) = (s16) M2C_FIELD(arg0, u8 *, 4);
    M2C_FIELD(temp_r6, s16 *, 0x16) = (s16) M2C_FIELD(arg0, u8 *, 5);
    M2C_FIELD(temp_r6, void **, 0x40) = arg0;
    M2C_FIELD(temp_r6, s32 *, 0x30) = arg1;
    return temp_r0;
}
