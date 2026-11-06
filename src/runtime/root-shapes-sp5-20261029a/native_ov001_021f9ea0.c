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
extern u32 native_fn_0203d294();
extern u32 native_fn_ov001_021dbaac();
typedef struct {
    u8 unknown_0[0x34];
    s32 field_34;
    u8 unknown_38[0x8];
    s32 field_40;
} Record_native_data_ov001_02239a14;
extern Record_native_data_ov001_02239a14 native_data_ov001_02239a14 __attribute__((aligned(2)));
u32 native_ov001_021f9ea0(void) {
    if (native_fn_ov001_021dbaac(native_data_ov001_02239a14.field_34) != 0) {
        return 0U;
    }
    if (native_fn_ov001_021dbaac(native_data_ov001_02239a14.field_40) != 0) {
        return 0U;
    }
    if ((s32) native_fn_0203d294(0x64) < 0x32) {
        return 0U;
    }
    return 1U;
}
