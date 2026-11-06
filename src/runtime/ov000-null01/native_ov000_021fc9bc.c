#define NULL ((void *)0)
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
extern u32 native_fn_0202a498();
extern u32 native_fn_ov000_021fcce4();
extern u32 native_fn_ov000_021fdde0();
extern u32 native_fn_ov000_021fde90();
extern u32 native_fn_ov000_022162b4();
extern u32 native_fn_ov000_02217440();
extern u8 native_data_ov000_022372a8[];
u32 native_ov000_021fc9bc(void) {
    u8 *temp_r4;

    temp_r4 = native_fn_ov000_02217440();
    if (M2C_FIELD(native_data_ov000_022372a8, s32 **, 0xC) == NULL) {
        return 0U;
    }
    native_fn_ov000_021fde90();
    native_fn_ov000_021fcce4(*M2C_FIELD(native_data_ov000_022372a8, s32 **, 0xC));
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 0x7F);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 2);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 0xC);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 0);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 5);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 6);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 7);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 8);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 0xD);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 0xE);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 0xF);
    native_fn_ov000_021fdde0();
    native_fn_0202a498(2, M2C_FIELD(native_data_ov000_022372a8, s32 **, 0xC));
    M2C_FIELD(native_data_ov000_022372a8, s32 **, 0xC) = NULL;
    return 0U;
}
