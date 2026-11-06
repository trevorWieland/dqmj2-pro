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
extern u32 native_fn_ov001_021f6cec();
extern u32 native_fn_ov001_021f71ec();
extern u32 native_fn_ov001_021f7498();
extern u32 native_fn_ov001_021f74fc();
extern u32 native_fn_ov001_021f7908();
extern u32 native_fn_ov001_021f80ac();
extern u32 native_fn_ov001_021f80fc();
extern u32 native_fn_ov001_021f8130();
typedef struct {
    u8 unknown_0[0x50];
    u16 field_50;
} Record_native_data_ov001_0223989c;
extern Record_native_data_ov001_0223989c native_data_ov001_0223989c;
u32 native_ov001_021f8208(void) {
    switch ((s32) native_data_ov001_0223989c.field_50) {
    case 0x2E:
        return native_fn_ov001_021f6cec();
    case 0xA3:
    case 0x38:
        return native_fn_ov001_021f71ec();
    case 0xDF:
        return native_fn_ov001_021f7498();
    case 0xE2:
        return native_fn_ov001_021f74fc();
    case 0xDB:
        return native_fn_ov001_021f7908();
    case 0xE7:
        return native_fn_ov001_021f80fc();
    case 0xFC:
        return native_fn_ov001_021f80ac();
    case 0xC1:
        return native_fn_ov001_021f8130();
    default:
        return 0U;
    }
}
