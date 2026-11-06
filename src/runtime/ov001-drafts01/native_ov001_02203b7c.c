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
extern u32 native_fn_02041538();
extern u32 native_fn_02041814();
extern u32 native_fn_0206be20();
extern u32 native_fn_ov001_021fe54c();
extern u32 native_fn_ov001_02203aa8();
extern u32 native_fn_ov001_02203e60();
extern u32 native_fn_ov001_022079a4();
typedef struct {
    u8 field_0;
    s8 field_1;
    u8 unknown_2[0x6];
    s8 field_8;
} Record_native_data_ov001_0223d8ec;
extern Record_native_data_ov001_0223d8ec native_data_ov001_0223d8ec;
typedef struct {
    u8 field_0;
    s8 field_1;
} Record_native_data_ov001_0223d8fc;
extern Record_native_data_ov001_0223d8fc native_data_ov001_0223d8fc;
u32 native_ov001_02203b7c(void) {
    if (native_fn_02041814() == 1) {
        return 0U;
    }
    if ((s8) native_data_ov001_0223d8ec.field_0 == 0) {
        native_data_ov001_0223d8ec.field_1 = 0;
        native_fn_ov001_02203e60();
        native_data_ov001_0223d8fc.field_0 = (u8) native_fn_0206be20(0);
        native_data_ov001_0223d8fc.field_1 = (s8) native_fn_0206be20(1);
        native_data_ov001_0223d8ec.field_0 = 0xA;
    } else {
        native_fn_ov001_021fe54c(8, 0x7F);
        native_fn_ov001_021fe54c(8, 0x1C);
        native_fn_ov001_021fe54c(8, 0x1D);
        native_fn_ov001_02203aa8();
        native_fn_ov001_022079a4();
        native_fn_02041538(0, 2, 0xA);
        native_data_ov001_0223d8ec.field_8 = 5;
        native_data_ov001_0223d8ec.field_0 = 0;
    }
    return 0U;
}
