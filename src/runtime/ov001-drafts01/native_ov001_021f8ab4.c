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
extern u32 native_fn_ov001_021f83a4();
extern u32 native_fn_ov001_021f84a0();
extern u32 native_fn_ov001_021f8718();
extern u32 native_fn_ov001_021f892c();
typedef struct {
    u8 unknown_0[0x50];
    u16 field_50;
} Record_native_data_ov001_0223989c;
extern Record_native_data_ov001_0223989c native_data_ov001_0223989c;
u32 native_ov001_021f8ab4(void) {
    switch ((s32) native_data_ov001_0223989c.field_50) {
    case 0xA3:
    case 0x38:
    case 0x2E:
        native_fn_ov001_021f83a4();
        break;
    case 0x98:
    case 0x97:
        native_fn_ov001_021f84a0();
        break;
    case 0x9F:
    case 0x4E:
    case 0x2B:
        native_fn_ov001_021f8718();
        break;
    case 0xC3:
        native_fn_ov001_021f892c();
        break;
    }
    return 0U;
}
