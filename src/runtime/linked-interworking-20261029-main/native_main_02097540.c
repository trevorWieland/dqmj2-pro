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
extern u32 native_fn_020065f0();
extern u32 native_fn_020068c0();
extern u32 native_fn_0200698c();
extern u32 native_fn_02007074();
extern u32 native_fn_020977cc();
extern u8 native_data_021d18f0[];
extern u8 native_data_021d18f8[];
u32 native_main_02097540(void) {
    u32 var_r0;

    native_fn_02007074(M2C_FIELD(native_data_021d18f0, void **, 8) + 0x13D8);
    M2C_FIELD(M2C_FIELD(native_data_021d18f0, void **, 8), s32 *, 0x13F0) = 0;
    if ((M2C_FIELD(M2C_FIELD(native_data_021d18f0, void **, 8), s32 *, 0x1384) == 0) || (var_r0 = native_fn_020068c0(M2C_FIELD(native_data_021d18f0, void **, 8) + 0x1318), (var_r0 != 0))) {
        native_fn_020065f0(M2C_FIELD(native_data_021d18f0, void **, 8) + 0x1318, native_fn_020977cc, native_data_021d18f8, M2C_FIELD(native_data_021d18f0, void **, 8) + 0x1000, 0x1000, 0x10);
        var_r0 = native_fn_0200698c(M2C_FIELD(native_data_021d18f0, void **, 8) + 0x1318);
    }
    return var_r0;
}
