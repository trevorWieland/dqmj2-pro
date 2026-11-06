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
extern u32 native_fn_02026144();
extern u32 native_fn_02048a60();
extern u32 native_fn_020d0a14();
extern u32 native_fn_020d0a24();
extern u8 native_data_021d6b48[];
u32 native_main_020cffe4(void) {
    s32 var_r0;
    u32 temp_r0;
    u32 temp_r0_2;
    u32 var_r4;

    var_r4 = native_fn_020d0a24();
    var_r0 = 0;
    if ((s32) var_r4 > 1) {
        var_r0 = 1;
        var_r4 -= 1;
    }
    if (var_r0 != 0) {
        native_fn_02048a60(M2C_FIELD(native_data_021d6b48, void **, 8), 0xD0, native_fn_02026144(native_fn_020d0a14() * 0x48, (s32) var_r4) + 0x28);
        M2C_FIELD(M2C_FIELD(native_data_021d6b48, void **, 8), u32 *, 0x7C) = (u32) (M2C_FIELD(M2C_FIELD(native_data_021d6b48, void **, 8), u32 *, 0x7C) | 2);
        temp_r0_2 = M2C_FIELD(M2C_FIELD(native_data_021d6b48, void **, 4), u32 *, 0x7C) & ~2;
        M2C_FIELD(M2C_FIELD(native_data_021d6b48, void **, 4), u32 *, 0x7C) = temp_r0_2;
        return temp_r0_2;
    }
    native_fn_02048a60(M2C_FIELD(native_data_021d6b48, void **, 4), 0xD0, native_fn_02026144(native_fn_020d0a14() * 0x48, (s32) var_r4) + 0x28);
    M2C_FIELD(M2C_FIELD(native_data_021d6b48, void **, 4), u32 *, 0x7C) = (u32) (M2C_FIELD(M2C_FIELD(native_data_021d6b48, void **, 4), u32 *, 0x7C) | 2);
    temp_r0 = M2C_FIELD(M2C_FIELD(native_data_021d6b48, void **, 8), u32 *, 0x7C) & ~2;
    M2C_FIELD(M2C_FIELD(native_data_021d6b48, void **, 8), u32 *, 0x7C) = temp_r0;
    return temp_r0;
}
