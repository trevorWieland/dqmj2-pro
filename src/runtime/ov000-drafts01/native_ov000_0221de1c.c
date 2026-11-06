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
extern u32 native_fn_02048a60();
extern u8 native_data_ov000_02246318[];
extern u8 native_data_ov000_02246348[];
u32 native_ov000_0221de1c(void *arg0, s32 arg1) {
    u32 temp_r0;
    u32 temp_r0_2;

    if (((u32) (u8) (s8) (M2C_FIELD(arg0, s8 *, 0x10) - 1) <= 2U) && (*native_data_ov000_02246318 == 0)) {
        if (arg1 != 0) {
            native_fn_02048a60(M2C_FIELD(native_data_ov000_02246348, void **, 0x24), 0x40, 0x60);
        } else {
            native_fn_02048a60(M2C_FIELD(native_data_ov000_02246348, void **, 0x24), 0x40, 0x50);
        }
        temp_r0_2 = M2C_FIELD(M2C_FIELD(native_data_ov000_02246348, void **, 0x24), u32 *, 0x7C) | 2;
        M2C_FIELD(M2C_FIELD(native_data_ov000_02246348, void **, 0x24), u32 *, 0x7C) = temp_r0_2;
        return temp_r0_2;
    }
    temp_r0 = M2C_FIELD(M2C_FIELD(native_data_ov000_02246348, void **, 0x24), u32 *, 0x7C) & ~2;
    M2C_FIELD(M2C_FIELD(native_data_ov000_02246348, void **, 0x24), u32 *, 0x7C) = temp_r0;
    return temp_r0;
}
