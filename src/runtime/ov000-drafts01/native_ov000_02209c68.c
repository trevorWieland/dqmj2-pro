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
extern u32 native_fn_020c56b4();
u32 native_ov000_02209c68(void *arg0, u8 arg1) {
    u8 temp_r4;

    temp_r4 = M2C_FIELD(arg0, u8 *, 0x278);
    M2C_FIELD(arg0, u8 *, 0x278) = arg1;
    M2C_FIELD(arg0, s8 *, 0x279) = 0;
    M2C_FIELD(arg0, s16 *, 0x27A) = 0;
    if (M2C_FIELD((void *) native_fn_020c56b4(M2C_FIELD(arg0, s16 *, 0x276)), u8 *, 7) == 6) {
        if ((arg1 == 4) && (temp_r4 != 3)) {
            M2C_FIELD(arg0, u8 *, 0x278) = 6U;
        } else if ((arg1 == 3) && (temp_r4 == 7)) {
            M2C_FIELD(arg0, u8 *, 0x278) = 5U;
        } else if ((arg1 == 3) && (temp_r4 == 8)) {
            M2C_FIELD(arg0, u8 *, 0x278) = 5U;
        } else if ((arg1 == 9) && (M2C_FIELD((void *) native_fn_020c56b4(M2C_FIELD(arg0, s16 *, 0x276)), u8 *, 0xA) == 7)) {
            M2C_FIELD(arg0, u8 *, 0x278) = temp_r4;
        }
    }
    return (u32) temp_r4;
}
