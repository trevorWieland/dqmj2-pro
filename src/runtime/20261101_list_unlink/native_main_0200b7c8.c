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
#define NULL ((void *)0)
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
typedef struct {
    s32 field_0;
    s32 field_4;
    s16 field_8;
    s16 field_a;
    s32 field_c;
} Record_native_data_020e5348;
extern Record_native_data_020e5348 native_data_020e5348;
u32 native_main_0200b7c8(u32 arg0) {
    u32 temp_r0;
    u32 temp_r0_2;
    void *temp_r2;
    void *temp_r2_2;

    temp_r0_2 = M2C_FIELD(arg0, u32 *, 0);
    if (temp_r0_2 == 0) {
        return temp_r0_2;
    }
    temp_r0 = native_fn_02007ff4();
    temp_r2 = M2C_FIELD(arg0, void **, 4);
    if (temp_r2 != NULL) {
        M2C_FIELD(temp_r2, void **, 8) = (void *) M2C_FIELD(arg0, void **, 8);
    }
    temp_r2_2 = M2C_FIELD(arg0, void **, 8);
    if (temp_r2_2 != NULL) {
        M2C_FIELD(temp_r2_2, void **, 4) = (void *) M2C_FIELD(arg0, void **, 4);
    }
    M2C_FIELD(arg0, u32 *, 0) = 0U;
    M2C_FIELD(arg0, void **, 8) = NULL;
    M2C_FIELD(arg0, void **, 4) = NULL;
    M2C_FIELD(arg0, s32 *, 0x1C) = (s32) (M2C_FIELD(arg0, s32 *, 0x1C) & ~1);
    if (native_data_020e5348.field_4 == arg0) {
        native_data_020e5348.field_4 = (s32) native_data_020e5348.field_0;
        native_data_020e5348.field_c = 0;
        native_data_020e5348.field_a = 0;
        native_data_020e5348.field_8 = 0;
    }
    return native_fn_02008008(temp_r0);
}
