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
extern u32 native_fn_ov001_021d9494();
extern u32 native_fn_ov001_021d9534();
extern u32 native_fn_ov001_021f1d54();
extern u8 native_data_ov001_02242b94[];
u32 native_ov001_02214968(void) {
    s32 temp_r4;

    if ((s8) M2C_FIELD(native_data_ov001_02242b94, u8 *, 0) == 0) {
        native_fn_ov001_021f1d54(5);
        native_fn_ov001_021d9494(M2C_FIELD(native_data_ov001_02242b94, void **, 8), 3, 1);
        M2C_FIELD(native_data_ov001_02242b94, u8 *, 0) = 0xA;
    } else if ((s8) M2C_FIELD(native_data_ov001_02242b94, u8 *, 0) == 0xA) {
        temp_r4 = *M2C_FIELD(M2C_FIELD(native_data_ov001_02242b94, void **, 8), s32 **, 0x60);
        if (native_fn_ov001_021d9534(M2C_FIELD(native_data_ov001_02242b94, void **, 8), -1, 6, 0) <= (u32) (temp_r4 >> 0xC)) {
            M2C_FIELD(native_data_ov001_02242b94, u8 *, 0) = 0x64;
        }
    } else {
        native_fn_ov001_021d9494(M2C_FIELD(native_data_ov001_02242b94, void **, 8), 0, 0);
        M2C_FIELD(native_data_ov001_02242b94, u8 *, 0) = 0;
        M2C_FIELD(native_data_ov001_02242b94, s8 *, 3) = 3;
    }
    return 0U;
}
