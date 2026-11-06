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
extern u32 native_fn_0202a634();
extern u32 native_fn_02048308();
extern u32 native_fn_0204baec();
extern u32 native_fn_0204bb28();
extern u32 native_fn_020834e8();
extern u32 native_fn_020851a8();
extern u32 native_fn_020ba574();
extern u32 native_fn_ov001_021f106c();
typedef struct {
    u8 unknown_0[0x8];
    s32 field_8;
} Record_native_data_ov001_02238f58;
extern Record_native_data_ov001_02238f58 native_data_ov001_02238f58;
u32 native_ov001_021f10c8(void) {
    native_fn_0202a634();
    native_fn_02048308();
    native_data_ov001_02238f58.field_8 = (s32) (native_data_ov001_02238f58.field_8 + 1);
    if (native_fn_ov001_021f106c() != 0) {
        if (native_fn_0204baec() == 0) {
            native_fn_020834e8();
            native_fn_0204bb28();
        } else {
            native_fn_020ba574();
            native_fn_0204bb28();
        }
    }
    return native_fn_020851a8();
}
