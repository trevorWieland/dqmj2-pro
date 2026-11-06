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
extern u32 native_fn_0205ccb8();
extern u32 native_fn_0205ce38();
typedef struct {
    u8 unknown_0[0x60];
    s16 field_60;
} Record_native_data_ov001_022316bc;
extern Record_native_data_ov001_022316bc native_data_ov001_022316bc;
u32 native_ov001_021d8c5c(void) {
    s32 temp_r0;
    u32 var_r4;

    var_r4 = 0;
    if (native_data_ov001_022316bc.field_60 != 0) {
        temp_r0 = (s32) native_fn_0205ccb8(native_data_ov001_022316bc.field_60, 0x1400);
        if (temp_r0 >= 0) {
            native_fn_0205ce38(temp_r0, 0x4800);
            var_r4 = 1;
        }
    }
    return var_r4;
}
