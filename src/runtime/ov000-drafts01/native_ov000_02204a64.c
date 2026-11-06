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
extern u32 native_fn_02061944();
extern u32 native_fn_0206e284();
typedef struct {
    u8 unknown_0[0x6];
    u8 field_6;
} Record_native_data_ov000_02238190;
extern Record_native_data_ov000_02238190 native_data_ov000_02238190;
u32 native_ov000_02204a64(void) {
    M2C_FIELD((void *) native_fn_02061944(), s8 *, 0x26A) = 0;
    if (native_data_ov000_02238190.field_6 != 0) {
        return (u32) native_data_ov000_02238190.field_6;
    }
    return native_fn_0206e284();
}
