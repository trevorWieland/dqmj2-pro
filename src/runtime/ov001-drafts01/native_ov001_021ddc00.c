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
extern u32 native_fn_0204446c();
extern u32 native_fn_ov001_021dd19c();
extern u32 native_fn_ov001_021dda80();
extern u32 native_fn_ov001_021f112c();
extern u32 native_fn_ov001_021ff238();
extern u32 native_fn_ov001_02210bf0();
typedef struct {
    u8 unknown_0[0x8];
    s8 field_8;
} Record_native_data_ov001_022388ec;
extern Record_native_data_ov001_022388ec native_data_ov001_022388ec;
u32 native_ov001_021ddc00(void) {
    native_fn_ov001_02210bf0();
    native_fn_ov001_021f112c(0);
    native_fn_ov001_021dd19c();
    if (native_fn_0204446c() != 0) {
        if (native_fn_ov001_021dda80() != 0) {
            native_fn_ov001_021ff238(0);
            native_data_ov001_022388ec.field_8 = 0x36;
        } else {
            native_data_ov001_022388ec.field_8 = 1;
        }
    } else {
        native_data_ov001_022388ec.field_8 = 0x24;
    }
    return 1U;
}
