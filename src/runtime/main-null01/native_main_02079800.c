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
extern u32 native_fn_0206006c();
extern u32 native_fn_ov000_02217418();
extern u32 native_fn_ov000_022174a8();
typedef struct {
    u8 unknown_0[0x10];
    s16 field_10;
    s16 field_12;
    s16 field_14;
    s16 field_16;
} Record_native_data_021c6544;
extern Record_native_data_021c6544 native_data_021c6544;
u32 native_main_02079800(void) {
    u32 temp_r0;
    u8 *temp_r0_3;
    void *temp_r0_2;
    void *temp_r3;
    u32 temp_r4;

    temp_r0_3 = native_fn_02049ad0(0xC);
    temp_r0_2 = M2C_FIELD(temp_r0_3, void **, 0);
    if (temp_r0_2 == NULL) {
        return (u32) temp_r0_2;
    }
    temp_r0 = native_fn_ov000_022174a8(M2C_FIELD(temp_r0_3, s8 *, 5));
    temp_r4 = temp_r0;
    temp_r3 = M2C_FIELD(M2C_FIELD(temp_r0_3, void **, 0), void **, 4);
    if (temp_r3 == NULL) {
        return temp_r0;
    }
    native_fn_02045dc4(1, M2C_FIELD(temp_r3, u8 *, 0x30), M2C_FIELD(temp_r3, u8 *, 0x1C), M2C_FIELD(temp_r3, u8 *, 0x1D), (s32) M2C_FIELD(temp_r3, u8 *, 0x1E), (s32) M2C_FIELD(temp_r3, u8 *, 0x1F));
    return native_fn_0206006c(native_fn_ov000_02217418(temp_r4), (s8) native_data_021c6544.field_10, (s8) native_data_021c6544.field_12, (s8) native_data_021c6544.field_14, (s32) (s8) native_data_021c6544.field_16);
}
