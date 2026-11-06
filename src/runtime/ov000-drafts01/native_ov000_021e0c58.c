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
extern u32 native_fn_020404e0();
extern u32 native_fn_ov000_021e7b9c();
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
} Record_native_data_ov000_0222ebec;
extern Record_native_data_ov000_0222ebec native_data_ov000_0222ebec;
extern u8 native_data_ov000_022322d4[];
u32 native_ov000_021e0c58(void) {
    u32 var_r0;
    u8 temp_r0;

    var_r0 = native_fn_020404e0();
    if (var_r0 == 5) {
        var_r0 = (u32) native_data_ov000_022322d4;
        if (M2C_FIELD((u32) native_data_ov000_022322d4, u8 *, 0x278) == 5) {
            temp_r0 = M2C_FIELD((u32) native_data_ov000_022322d4, u8 *, 0x161);
            if (temp_r0 & 0xE) {
                return (u32) temp_r0;
            }
            return native_fn_ov000_021e7b9c(native_data_ov000_0222ebec.field_4);
        }
    }
    return var_r0;
}
