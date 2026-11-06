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
extern u32 native_fn_02008430();
extern u32 native_fn_02008c58();
extern u32 native_fn_0202a37c();
extern u32 native_fn_02048e74();
extern u32 native_fn_02048fcc();
extern u32 native_fn_020c1e8c();
extern u32 native_fn_020d349c();
extern u32 native_fn_020d3dc0();
extern u32 native_fn_020d3e20();
extern u32 native_fn_ov000_021f33ac();
extern u32 native_fn_ov000_021f33d4();
typedef struct {
    u8 unknown_0[0x8];
    u32 field_8;
} Record_native_data_ov000_02236d98;
extern Record_native_data_ov000_02236d98 native_data_ov000_02236d98;
void native_ov000_021f0638(void) {
    u32 temp_r0;
    u32 temp_r8;
    u8 var_r10;

    if (native_data_ov000_02236d98.field_8 == 0) {
        native_data_ov000_02236d98.field_8 = native_fn_0202a37c(2, 0x1924, 4);
    }
    native_fn_02008c58(0, native_data_ov000_02236d98.field_8, 0x1924);
    native_fn_02048e74(native_data_ov000_02236d98.field_8, 4);
    native_fn_02048fcc(native_data_ov000_02236d98.field_8 + 0x10);
    native_fn_020c1e8c();
    native_fn_ov000_021f33ac();
    if (native_fn_ov000_021f33d4(2) == 0) {
        native_fn_02008430();
    }
    native_fn_020d349c();
    var_r10 = 0;
    do {
        temp_r8 = native_fn_020d3dc0(1, var_r10);
        temp_r0 = native_fn_020d3e20(1, var_r10);
        if (temp_r8 != -1U) {
            M2C_FIELD((native_data_ov000_02236d98.field_8 + (var_r10 * 4)), s16 *, 0x190C) = (s16) temp_r8;
            M2C_FIELD((native_data_ov000_02236d98.field_8 + (var_r10 * 4)), s8 *, 0x190E) = (s8) temp_r0;
            native_fn_020d3e20(1, var_r10);
        } else {
            M2C_FIELD((native_data_ov000_02236d98.field_8 + (var_r10 * 4)), s16 *, 0x190C) = 0;
            M2C_FIELD((native_data_ov000_02236d98.field_8 + (var_r10 * 4)), s8 *, 0x190E) = 0;
        }
        var_r10 += 1;
    } while ((u32) var_r10 < 3U);
}
