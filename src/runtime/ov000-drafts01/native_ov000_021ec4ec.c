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
extern u32 native_fn_02004120();
extern u32 native_fn_02004174();
extern u32 native_fn_02008430();
extern u32 native_fn_02008c58();
extern u32 native_fn_0202a37c();
extern u32 native_fn_02048e74();
extern u32 native_fn_02048fcc();
extern u32 native_fn_0208474c();
extern u32 native_fn_02084764();
typedef struct {
    u8 field_0;
    u8 unknown_1[0x3];
    u32 field_4;
} Record_native_data_ov000_02236bc4;
extern Record_native_data_ov000_02236bc4 native_data_ov000_02236bc4;
u32 native_ov000_021ec4ec(void) {
    u32 temp_r0;

    native_fn_02008c58(0, native_fn_02004120(), 0x8000);
    native_fn_02008c58(0, native_fn_02004174(), 0x8000);
    if (native_data_ov000_02236bc4.field_4 == 0) {
        native_data_ov000_02236bc4.field_4 = native_fn_0202a37c(2, 0x51C, 4);
    }
    native_fn_02008c58(0, native_data_ov000_02236bc4.field_4, 0x51C);
    native_fn_02048e74(native_data_ov000_02236bc4.field_4, 2);
    native_fn_02048fcc(native_data_ov000_02236bc4.field_4 + 0x10);
    native_fn_0208474c();
    temp_r0 = native_fn_02084764(2, native_data_ov000_02236bc4.field_0);
    if (temp_r0 != 0) {
        return temp_r0;
    }
    return native_fn_02008430();
}
