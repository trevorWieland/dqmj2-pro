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
extern u8 native_data_ov006_0221c0d8[];
u32 native_ov006_021f893c(s32 arg0, s32 arg1) {
    s32 var_r0;
    s32 temp_r1;
    s32 temp_r2;
    void *temp_r2_2;
    void *temp_r6;

    var_r0 = arg0;
    if (var_r0 < (s32) M2C_FIELD(M2C_FIELD(native_data_ov006_0221c0d8, void **, 4), u8 *, 0x51)) {
        temp_r2 = arg1 * 4;
        temp_r6 = M2C_FIELD((M2C_FIELD(native_data_ov006_0221c0d8, void **, 4) + temp_r2), void **, 0x10);
        temp_r1 = 0x2A * var_r0;
        M2C_FIELD(temp_r6, u16 *, 4) = (u16) (M2C_FIELD((M2C_FIELD(native_data_ov006_0221c0d8, void **, 4) + (M2C_FIELD((M2C_FIELD(M2C_FIELD(native_data_ov006_0221c0d8, void **, 4), s32 *, 0) + temp_r1), u8 *, 0x28) * 2)), u16 *, 0x42) | (M2C_FIELD(temp_r6, u16 *, 4) & 0xFFFFFC00));
        temp_r2_2 = M2C_FIELD((M2C_FIELD(native_data_ov006_0221c0d8, void **, 4) + temp_r2), void **, 0x24);
        var_r0 = (0xFFFFFC00 & M2C_FIELD(temp_r2_2, u16 *, 4)) | M2C_FIELD((M2C_FIELD(native_data_ov006_0221c0d8, void **, 4) + (M2C_FIELD((M2C_FIELD(M2C_FIELD(native_data_ov006_0221c0d8, void **, 4), s32 *, 0) + temp_r1), u16 *, 0x26) * 2)), u16 *, 0x48);
        M2C_FIELD(temp_r2_2, u16 *, 4) = (u16) var_r0;
    }
    return (u32) var_r0;
}
