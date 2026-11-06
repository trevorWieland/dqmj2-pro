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
extern u32 native_fn_02084f4c();
typedef struct {
    u8 unknown_0[0x24];
    s32 field_24;
} Record_native_data_ov006_0220e9a0;
extern Record_native_data_ov006_0220e9a0 native_data_ov006_0220e9a0;
extern u8 native_data_ov006_0220eb04[];
u32 native_ov006_021d7de4(void) {
    s32 var_r6;

    var_r6 = 0;
    if ((s32) native_data_ov006_0220e9a0.field_24 <= 0) {
        return (u32) native_data_ov006_0220e9a0.field_24;
    }
    do {
        native_fn_02084f4c(*(u32 *)(native_data_ov006_0220eb04 + (var_r6 * 4)));
        var_r6 += 1;
    } while (var_r6 < (s32) native_data_ov006_0220e9a0.field_24);
    return (u32) native_data_ov006_0220e9a0.field_24;
}
