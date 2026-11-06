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
extern u32 native_fn_02044ff4();
extern u32 native_fn_02048034();
extern u32 native_fn_02063520();
extern u32 native_fn_02063574();
extern u32 native_fn_020635d4();
extern u32 native_fn_02063628();
extern u32 native_fn_020bf218();
u32 native_ov005_021e13a4(s32 arg0) {
    s16 temp_r0_2;
    u32 temp_r0;
    u32 temp_r4;
    s32 temp_r5;
    u8 sp0[32];

    temp_r0 = native_fn_020bf218();
    if (arg0 >= 3) {
        return 0U;
    }
    temp_r5 = (arg0 * 0x84) + (temp_r0 + 0xC4);
    temp_r0_2 = M2C_FIELD(temp_r5, s16 *, 0x18);
    if (temp_r0_2 != 0) {
        temp_r4 = native_fn_02063520(temp_r0_2, M2C_FIELD(temp_r5, u8 *, 0x1A));
        if ((temp_r4 | (native_fn_020635d4(M2C_FIELD(temp_r5, s16 *, 0x18), M2C_FIELD(temp_r5, u8 *, 0x1A)) * 2)) != 3) {
            native_fn_02063628(M2C_FIELD(temp_r5, s16 *, 0x18), M2C_FIELD(temp_r5, u8 *, 0x1A));
            native_fn_02063574(M2C_FIELD(temp_r5, s16 *, 0x18), M2C_FIELD(temp_r5, u8 *, 0x1A));
            native_fn_02044ff4(&sp0, M2C_FIELD(temp_r5, s16 *, 0x18), M2C_FIELD(temp_r5, u8 *, 0x1A));
            native_fn_02048034(&sp0, 0);
            return (u32) M2C_FIELD(temp_r5, s16 *, 0x18);
        }
    }
    return 0U;
}
