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
extern u32 native_fn_ov001_021db618();
extern u32 native_fn_ov001_021f949c();
extern u32 native_fn_ov001_021f9ea0();
extern u32 native_fn_ov001_021f9ef0();
extern u8 native_data_ov001_02239a14[];
u32 native_ov001_021fa06c(void) {
    if (M2C_FIELD(native_data_ov001_02239a14, u8 *, 5) == 0) {
        native_fn_ov001_021db618(M2C_FIELD(native_data_ov001_02239a14, void **, 0x34), M2C_FIELD(native_data_ov001_02239a14, s32 *, 0x40));
        native_fn_ov001_021d9494(M2C_FIELD(native_data_ov001_02239a14, void **, 0x34), 1, 0);
        if (M2C_FIELD(native_data_ov001_02239a14, u8 *, 0xC) == 3) {
            M2C_FIELD(native_data_ov001_02239a14, u8 *, 0xC) = (u8) native_fn_ov001_021f9ea0();
        }
        native_fn_ov001_021f9ef0(M2C_FIELD(native_data_ov001_02239a14, u8 *, 0xC));
        native_fn_ov001_021f949c(0xDD, 1);
        M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x2C) = (s16) ((s32) *M2C_FIELD(M2C_FIELD(native_data_ov001_02239a14, void **, 0x34), s32 **, 0x60) >> 0xC);
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 5) = 0xAU;
    }
    if ((M2C_FIELD(native_data_ov001_02239a14, u8 *, 5) == 0xA) && ((native_fn_ov001_021d9534(M2C_FIELD(native_data_ov001_02239a14, void **, 0x34), -1, 1, M2C_FIELD(native_data_ov001_02239a14, s16 *, 0x2C)) - 5) == ((s32) *M2C_FIELD(M2C_FIELD(native_data_ov001_02239a14, void **, 0x34), s32 **, 0x60) >> 0xC))) {
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 5) = 0x64U;
    }
    if (M2C_FIELD(native_data_ov001_02239a14, u8 *, 5) == 0x64) {
        M2C_FIELD(native_data_ov001_02239a14, u8 *, 5) = 0U;
        M2C_FIELD(native_data_ov001_02239a14, s8 *, 0xA) = 7;
    }
    return 0U;
}
