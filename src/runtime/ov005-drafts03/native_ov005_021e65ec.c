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
extern u32 native_fn_0202a37c();
extern u32 native_fn_0202a498();
extern u32 native_fn_0202a818();
extern u32 native_fn_02044f9c();
extern u8 native_data_ov005_021e7884[];
u32 native_ov005_021e65ec(u32 arg0, u32 arg1, u32 arg2) {
    u32 temp_r0;
    u32 temp_r5;

    temp_r5 = native_fn_02044f9c();
    temp_r0 = native_fn_0202a37c(arg2, 0x190, 4);
    if (temp_r0 == 0) {
        goto block_4;
    }
    if (native_fn_0202a818(native_data_ov005_021e7884, temp_r0, 0x190, temp_r5 * 0x190) == 0) {
        goto block_3;
    }
    return temp_r0;
block_3:
    native_fn_0202a498(arg2, temp_r0);
block_4:
    return 0U;
}
