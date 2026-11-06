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
extern u32 native_fn_02041814();
extern u32 native_fn_ov001_021fc390();
extern u32 native_fn_ov001_021fd288();
extern u32 native_fn_ov001_021fe74c();
typedef struct {
    u8 unknown_0[0xa];
    s8 field_a;
    u8 unknown_b[0x31];
    s32 field_3c;
} Record_native_data_ov001_02239c10;
extern Record_native_data_ov001_02239c10 native_data_ov001_02239c10;
u32 native_ov001_0220208c(void) {
    if (native_fn_02041814() == 1) {
        return 0U;
    }
    if (native_data_ov001_02239c10.field_3c == 0) {
        native_fn_ov001_021fe74c(0);
        native_fn_ov001_021fd288();
        native_fn_ov001_021fc390();
        native_data_ov001_02239c10.field_a = 0;
    }
    return 0U;
}
