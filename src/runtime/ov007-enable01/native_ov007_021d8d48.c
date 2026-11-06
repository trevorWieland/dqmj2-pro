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
extern u32 native_fn_02048a44();
extern u32 native_fn_ov007_021d873c();
typedef struct {
    u8 unknown_0[0xc];
    s32 field_c;
} Record_native_data_ov007_021da9dc;
extern Record_native_data_ov007_021da9dc native_data_ov007_021da9dc;
u32 native_ov007_021d8d48(void) {
    s32 var_r0;
    u32 temp_r0;
    void *var_r1;
    s32 var_r4;
    s32 var_r5;

    var_r4 = 0;
    var_r5 = 0;
    do {
        if (native_fn_ov007_021d873c(var_r4) != 0) {
            var_r1 = native_data_ov007_021da9dc.field_c + var_r5;
            var_r0 = M2C_FIELD(var_r1, s32 *, 0x7C) | 2;
        } else {
            var_r1 = native_data_ov007_021da9dc.field_c + var_r5;
            var_r0 = M2C_FIELD(var_r1, s32 *, 0x7C) & ~2;
        }
        M2C_FIELD(var_r1, s32 *, 0x7C) = var_r0;
        temp_r0 = native_fn_02048a44(native_data_ov007_021da9dc.field_c + var_r5 + 8, 1);
        var_r4 += 1;
        var_r5 += 0x90;
    } while (var_r4 < 0x10);
    return temp_r0;
}
