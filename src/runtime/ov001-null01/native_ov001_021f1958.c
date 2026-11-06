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
extern u32 native_fn_0205ff4c();
extern u32 native_fn_0208527c();
extern u32 native_fn_ov001_021f19f0();
typedef struct {
    u8 unknown_0[0x28];
    s32 field_28;
} Record_native_data_ov001_02238f58;
extern Record_native_data_ov001_02238f58 native_data_ov001_02238f58;
u32 native_ov001_021f1958(void) {
    u8 *temp_r0_2;
    void *temp_r0;
    void *temp_r5;

    temp_r0_2 = native_fn_ov001_021f19f0();
    temp_r0 = M2C_FIELD(temp_r0_2, void **, 0);
    if (temp_r0 != NULL) {
        temp_r5 = M2C_FIELD(temp_r0, void **, 4);
        if (temp_r5 != NULL) {
            native_fn_0208527c(temp_r5 + 0x3C, M2C_FIELD(temp_r5, u8 *, 0x1E));
            native_data_ov001_02238f58.field_28 = (s32) (native_data_ov001_02238f58.field_28 - (M2C_FIELD(temp_r5, u8 *, 0x5E) * M2C_FIELD(temp_r5, u8 *, 0x5F)));
            native_fn_02045dc4(0, M2C_FIELD(temp_r5, u8 *, 0x30), M2C_FIELD(temp_r5, u8 *, 0x1C), M2C_FIELD(temp_r5, u8 *, 0x1D), (s32) M2C_FIELD(temp_r5, u8 *, 0x1E), (s32) M2C_FIELD(temp_r5, u8 *, 0x1F));
            native_fn_0205ff4c(M2C_FIELD(temp_r0_2, void **, 0));
            M2C_FIELD(temp_r0_2, void **, 0) = NULL;
            M2C_FIELD(temp_r0_2, s8 *, 6) = -1;
            return -1U;
        }
    }
    return (u32) temp_r0;
}
