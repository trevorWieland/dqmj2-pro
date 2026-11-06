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
extern u32 native_fn_02049ad0();
extern u32 native_fn_0205ff4c();
extern u32 native_fn_02086b14();
extern u32 native_fn_ov000_021f03e8();
typedef struct {
    u8 unknown_0[0x18];
    s32 field_18;
} Record_native_data_ov000_02236c1c;
extern Record_native_data_ov000_02236c1c native_data_ov000_02236c1c;
u32 native_ov000_021f0448(void) {
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
        native_data_ov000_02236c1c.field_18 = (s32) (native_data_ov000_02236c1c.field_18 - (M2C_FIELD(temp_r1, u8 *, 0x1E) * M2C_FIELD(temp_r1, u8 *, 0x1F)));
    }
    native_fn_ov000_021f03e8(temp_r0_2);
    native_fn_02086b14(M2C_FIELD(M2C_FIELD(temp_r0_2, void **, 0), void **, 4), 0);
    native_fn_0205ff4c(M2C_FIELD(temp_r0_2, void **, 0));
    M2C_FIELD(temp_r0_2, void **, 0) = NULL;
    M2C_FIELD(temp_r0_2, s8 *, 6) = -1;
    return -1U;
}
