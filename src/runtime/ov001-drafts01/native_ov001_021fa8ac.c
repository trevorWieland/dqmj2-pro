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
extern u32 native_fn_ov001_02210ad0();
typedef struct {
    u8 unknown_0[0x22];
    s16 field_22;
    u8 unknown_24[0x2];
    s16 field_26;
} Record_native_data_ov001_02239a14;
extern Record_native_data_ov001_02239a14 native_data_ov001_02239a14;
u32 native_ov001_021fa8ac(void *arg0, void *arg1) {
    u32 var_r4;

    var_r4 = 0;
    if (((s32) native_data_ov001_02239a14.field_26 < 0x3E8) && (M2C_FIELD(M2C_FIELD(arg1, void **, 0x1E8), u8 *, 0xA6) != 0) && (((s32) native_fn_0207b674(0x33, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) || ((s32) native_fn_0207b674(0x4E, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0) || ((s32) native_fn_0207b674(0x59, M2C_FIELD(arg0, s32 *, 0x1E8) + 0x46) > 0)) && ((s32) native_data_ov001_02239a14.field_22 >= 5) && (native_fn_ov001_02210ad0(arg0, 8, 1) != 0)) {
        var_r4 = 1;
    }
    return var_r4;
}
