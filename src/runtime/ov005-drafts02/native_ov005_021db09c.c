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
extern u32 native_fn_02008c58();
extern u32 native_fn_02048644();
extern u32 native_fn_02048a60();
extern u32 native_fn_02048a94();
extern u32 native_fn_02048a9c();
extern u32 native_fn_ov005_021da838();
typedef struct {
    u8 unknown_0[0x50];
    s32 field_50;
    s32 field_54;
} Record_native_data_ov005_021e9818;
extern Record_native_data_ov005_021e9818 native_data_ov005_021e9818;
extern u8 native_data_ov005_021eada8[];
void native_ov005_021db09c(u32 arg0, u32 arg1, u32 arg2) {
    s32 temp_r4;
    s32 temp_r1;

    temp_r4 = (native_data_ov005_021e9818.field_50 * 0x90) + (s32) native_data_ov005_021eada8;
    temp_r1 = temp_r4;
    native_data_ov005_021e9818.field_50 = (s32) (native_data_ov005_021e9818.field_50 + 1);
    native_fn_02008c58(0, temp_r1, 4);
    native_fn_ov005_021da838(temp_r4);
    native_fn_02048a9c(temp_r4, 3);
    native_fn_02048a94(temp_r4, 0);
    native_fn_02048a60(temp_r4, arg0, arg1);
    native_fn_02048644(temp_r4, native_data_ov005_021e9818.field_54, arg2);
    M2C_FIELD(temp_r4, s32 *, 0x7C) = (s32) (M2C_FIELD(temp_r4, s32 *, 0x7C) & ~2);
    return;
}
