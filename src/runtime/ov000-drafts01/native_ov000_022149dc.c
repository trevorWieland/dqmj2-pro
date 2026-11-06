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
extern u32 native_fn_ov000_0221480c();
extern u32 native_fn_ov000_02214970();
typedef struct {
    u8 unknown_0[0x10];
    s32 field_10;
} Record_native_data_ov000_02244efc;
extern Record_native_data_ov000_02244efc native_data_ov000_02244efc;
u32 native_ov000_022149dc(void) {
    u32 var_r4;

    var_r4 = 0;
    if (native_data_ov000_02244efc.field_10 == 0) {
        if (native_fn_ov000_0221480c() != 0) {
            native_data_ov000_02244efc.field_10 = 0xA;
        }
    } else if (native_data_ov000_02244efc.field_10 == 0xA) {
        native_fn_ov000_02214970();
        var_r4 = 1;
        native_data_ov000_02244efc.field_10 = 0;
    }
    return var_r4;
}
