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
extern u32 native_fn_ov001_022042ac();
extern u32 native_fn_ov001_02204c1c();
u32 native_ov001_02204b5c(void *arg0, s32 arg1, s16 arg2, s16 arg3) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r4;

    temp_r0 = native_fn_ov001_02204270();
    if (temp_r0 == 0x7F) {
        return temp_r0;
    }
    temp_r4 = native_fn_ov001_02204250();
    native_fn_ov001_02204244();
    M2C_FIELD(temp_r4, s8 *, 0x22) = 0x15;
    native_fn_ov001_022042ac(temp_r0);
    M2C_FIELD(temp_r4, s32 *, 0) = 7;
    M2C_FIELD(temp_r4, s16 *, 0x14) = arg2;
    M2C_FIELD(temp_r4, s16 *, 0x16) = arg3;
    M2C_FIELD(temp_r4, s8 *, 0x20) = 8;
    M2C_FIELD(temp_r4, s8 *, 0x21) = 3;
    M2C_FIELD(temp_r4, void **, 0x28) = arg0;
    M2C_FIELD(temp_r4, void **, 0x2C) = arg0;
    M2C_FIELD(temp_r4, s32 *, 0x30) = (s32) M2C_FIELD(arg0, s32 *, 0x200);
    M2C_FIELD(temp_r4, s32 *, 0x34) = arg1;
    M2C_FIELD(temp_r4, s32 *, 0x38) = (s32) M2C_FIELD(arg0, u8 *, 0x1FC);
    M2C_FIELD(temp_r4, s8 *, 0x24) = 0;
    temp_r0_2 = native_fn_ov001_02204c1c(0, 0xB0, (s16) (M2C_FIELD(temp_r4, s16 *, 0x16) - 0x1C), 1);
    if (temp_r0_2 != 0x7F) {
        M2C_FIELD((void *) native_fn_ov001_02204250(), s8 *, 8) = (s8) temp_r0;
        M2C_FIELD(temp_r4, s8 *, 9) = (s8) temp_r0_2;
    }
    return temp_r0;
}
