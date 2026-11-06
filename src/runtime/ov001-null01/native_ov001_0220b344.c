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
extern u32 native_fn_ov001_0220aa54();
typedef struct {
    u8 field_0;
    u8 unknown_1[0x3];
    s32 field_4;
} Record_native_data_ov001_0223df3c;
extern Record_native_data_ov001_0223df3c native_data_ov001_0223df3c;
u32 native_ov001_0220b344(void) {
    void *temp_r0;
    void *temp_r0_2;
    void *temp_r0_3;
    u8 *temp_r4;

    temp_r4 = native_fn_02049ad0();
    native_data_ov001_0223df3c.field_0 = (s8) native_data_ov001_0223df3c.field_0 - 1;
    temp_r0_2 = M2C_FIELD(temp_r4, void **, 0);
    if (temp_r0_2 == NULL) {
        return (u32) temp_r0_2;
    }
    temp_r0_3 = M2C_FIELD(temp_r0_2, void **, 4);
    native_data_ov001_0223df3c.field_4 = (s32) (native_data_ov001_0223df3c.field_4 - (M2C_FIELD(temp_r0_3, u8 *, 0x1E) * M2C_FIELD(temp_r0_3, u8 *, 0x1F)));
    temp_r0 = M2C_FIELD(temp_r4, void **, 0);
    if (temp_r0 == NULL) {
        return (u32) temp_r0;
    }
    native_fn_ov001_0220aa54(M2C_FIELD(temp_r4, s8 *, 5));
    native_fn_0205ff4c(M2C_FIELD(temp_r4, void **, 0));
    M2C_FIELD(temp_r4, void **, 0) = NULL;
    M2C_FIELD(temp_r4, s8 *, 6) = -1;
    return -1U;
}
