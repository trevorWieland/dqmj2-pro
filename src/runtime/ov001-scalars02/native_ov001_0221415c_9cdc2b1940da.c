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
extern u32 native_fn_ov001_02213da8();
extern u32 native_fn_ov001_02213ee0();
extern u32 native_fn_ov001_02214070();
typedef struct {
    u8 field_0;
    s8 field_1;
} Record_native_data_ov001_02242aac;
extern Record_native_data_ov001_02242aac native_data_ov001_02242aac;
extern u8 native_data_ov001_02242ab8[];
u32 native_ov001_0221415c(void) {
    u32 temp_r0;

    temp_r0 = *(u32 *)(native_data_ov001_02242ab8 + ((s8) native_data_ov001_02242aac.field_0 * 0xC));
    switch (temp_r0) {
    case 1:
        break;
    default:
        break;
    case 0:
        if (native_fn_ov001_02213da8() != 0) {
            native_data_ov001_02242aac.field_1 = 2;
        }
        break;
    case 2:
        if (native_fn_ov001_02213ee0() != 0) {
            native_data_ov001_02242aac.field_1 = 2;
        }
        break;
    case 3:
        if (native_fn_ov001_02214070() != 0) {
            native_data_ov001_02242aac.field_1 = 2;
        }
        break;
    }
    return 0U;
}
