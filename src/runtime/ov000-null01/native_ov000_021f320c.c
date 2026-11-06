#define NULL ((void *)0)
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
extern u32 native_fn_02045dc4();
extern u32 native_fn_02049ad0();
extern u32 native_fn_0205ff4c();
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
} Record_native_data_ov000_02236dbc;
extern Record_native_data_ov000_02236dbc native_data_ov000_02236dbc;
extern u8 native_data_ov000_02236dcf[];
u32 native_ov000_021f320c(void) {
    u8 *temp_r0_2;
    void *temp_r0;
    void *temp_r1;

    temp_r0_2 = native_fn_02049ad0();
    temp_r0 = M2C_FIELD(temp_r0_2, void **, 0);
    if (temp_r0 == NULL) {
        return (u32) temp_r0;
    }
    temp_r1 = M2C_FIELD(temp_r0, void **, 4);
    if (M2C_FIELD(temp_r1, s32 *, 0x60) != 0) {
        native_data_ov000_02236dbc.field_4 = (s32) (native_data_ov000_02236dbc.field_4 - (M2C_FIELD(temp_r1, u8 *, 0x1E) * M2C_FIELD(temp_r1, u8 *, 0x1F)));
    }
    native_fn_02045dc4(1, *(native_data_ov000_02236dcf + (M2C_FIELD(temp_r0_2, s8 *, 5) * 0xC)), M2C_FIELD(temp_r1, u8 *, 0x5C), M2C_FIELD(temp_r1, u8 *, 0x5D), (s32) M2C_FIELD(temp_r1, u8 *, 0x5E), (s32) M2C_FIELD(temp_r1, u8 *, 0x5F));
    native_fn_0205ff4c(M2C_FIELD(temp_r0_2, void **, 0));
    M2C_FIELD(temp_r0_2, void **, 0) = NULL;
    M2C_FIELD(temp_r0_2, s8 *, 6) = -1;
    return -1U;
}
