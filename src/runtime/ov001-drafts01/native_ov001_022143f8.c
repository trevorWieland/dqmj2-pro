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
extern u32 native_fn_0207b004();
extern u32 native_fn_ov001_021d7e80();
extern u32 ov001_begin_state_transition_021f1354();
extern u32 native_fn_ov001_021f1414();
extern u32 ov001_select_mode_id_021f1438();
extern u32 native_fn_ov001_02202528();
extern u8 native_data_ov001_02242b50[];
u32 native_ov001_022143f8(void) {
    ov001_begin_state_transition_021f1354(M2C_FIELD(native_data_ov001_02242b50, u8 *, 3), M2C_FIELD(native_data_ov001_02242b50, u8 *, 4), M2C_FIELD(native_data_ov001_02242b50, u16 *, 0xE), 1);
    if (M2C_FIELD(native_data_ov001_02242b50, s8 *, 5) == -1) {
        native_fn_ov001_021f1414(M2C_FIELD(M2C_FIELD(native_data_ov001_02242b50, void **, 0x10), u8 *, 0x31E));
        ov001_select_mode_id_021f1438();
    } else {
        ov001_select_mode_id_021f1438((u8) M2C_FIELD(native_data_ov001_02242b50, s8 *, 5));
    }
    native_fn_ov001_021d7e80(M2C_FIELD(native_data_ov001_02242b50, void **, 0x10));
    native_fn_ov001_02202528(M2C_FIELD(M2C_FIELD(native_data_ov001_02242b50, void **, 0x10), u8 *, 0x31E), M2C_FIELD(M2C_FIELD(native_data_ov001_02242b50, void **, 0x10), u8 *, 0x31F));
    if ((native_fn_0207b004(M2C_FIELD(native_data_ov001_02242b50, u16 *, 0xC), 0x04000000) != 0) && (M2C_FIELD(M2C_FIELD(native_data_ov001_02242b50, void **, 0x10), s8 *, 0x254) != 0) && (M2C_FIELD(native_data_ov001_02242b50, u8 *, 7) != 1)) {
        M2C_FIELD(native_data_ov001_02242b50, s8 *, 2) = 4;
    } else {
        M2C_FIELD(native_data_ov001_02242b50, s8 *, 2) = 2;
    }
    return 0U;
}
