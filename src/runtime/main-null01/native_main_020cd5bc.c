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
extern u32 native_fn_0206db90();
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
    s32 field_8;
} Record_native_data_021d6840;
extern Record_native_data_021d6840 native_data_021d6840;
extern u8 native_data_021d6873[];
u32 native_main_020cd5bc(void) {
    u32 temp_r0;
    u8 *temp_r0_2;
    void *temp_r1;
    void *temp_r2;
    void *temp_ip;

    temp_r0_2 = native_fn_02049ad0();
    temp_r0 = native_fn_0206db90(M2C_FIELD(temp_r0_2, s8 *, 5));
    temp_r2 = M2C_FIELD(M2C_FIELD(temp_r0_2, void **, 0), void **, 4);
    native_data_021d6840.field_4 = (s32) (native_data_021d6840.field_4 - (M2C_FIELD(temp_r2, u8 *, 0x1E) * M2C_FIELD(temp_r2, u8 *, 0x1F)));
    native_data_021d6840.field_8 = (s32) (native_data_021d6840.field_8 - 1);
    temp_r1 = M2C_FIELD(temp_r0_2, void **, 0);
    if (temp_r1 == NULL) {
        return temp_r0;
    }
    temp_ip = M2C_FIELD(temp_r1, void **, 4);
    if (temp_r0 != 0x7F) {
        native_fn_02045dc4(1, *(native_data_021d6873 + (temp_r0 * 0xC)), M2C_FIELD(temp_ip, u8 *, 0x5C), M2C_FIELD(temp_ip, u8 *, 0x5D), (s32) M2C_FIELD(temp_ip, u8 *, 0x5E), (s32) M2C_FIELD(temp_ip, u8 *, 0x5F));
    }
    native_fn_0205ff4c(M2C_FIELD(temp_r0_2, void **, 0));
    M2C_FIELD(temp_r0_2, void **, 0) = NULL;
    M2C_FIELD(temp_r0_2, s8 *, 6) = -1;
    return -1U;
}
