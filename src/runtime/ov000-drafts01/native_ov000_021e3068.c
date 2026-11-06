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
extern u32 native_fn_02040564();
extern u32 native_fn_0205c020();
extern u32 native_fn_0205c040();
extern u32 native_fn_ov000_021e0f84();
extern u32 native_fn_ov000_021e1894();
extern u32 native_fn_ov000_021e24d0();
extern u32 native_fn_ov000_021e25c0();
extern u32 native_fn_ov000_021e267c();
extern u32 native_fn_ov000_021e2744();
extern u32 native_fn_ov000_021e28d8();
extern u32 native_fn_ov000_021e2ba8();
extern u32 native_fn_ov000_021e2ce0();
extern u32 native_fn_ov000_021e3028();
extern u32 native_fn_ov000_021e31a4();
typedef struct {
    u8 unknown_0[0x8];
    s32 field_8;
} Record_native_data_ov000_022322c4;
extern Record_native_data_ov000_022322c4 native_data_ov000_022322c4;
typedef struct {
    u8 unknown_0[0x1e0];
    u8 field_1e0;
    u8 unknown_1e1[0x97];
    u8 field_278;
} Record_native_data_ov000_022322d4;
extern Record_native_data_ov000_022322d4 native_data_ov000_022322d4;
u32 native_ov000_021e3068(void) {
    if (native_fn_ov000_021e0f84() == 0) {
        switch (native_data_ov000_022322d4.field_278) {
        default:
            break;
        case 2:
            native_fn_ov000_021e24d0();
            break;
        case 3:
            native_fn_ov000_021e25c0();
            break;
        case 4:
            native_fn_ov000_021e267c();
            break;
        case 5:
            native_fn_ov000_021e2744();
            break;
        case 6:
            native_fn_ov000_021e28d8();
            break;
        case 7:
            native_fn_ov000_021e2ba8();
            break;
        case 8:
            native_fn_ov000_021e2ce0();
            break;
        }
        native_fn_ov000_021e3028();
        native_fn_0205c020(native_data_ov000_022322d4.field_278);
        native_fn_0205c040(native_data_ov000_022322d4.field_1e0);
        if ((native_fn_ov000_021e1894(1) == 0) && (native_data_ov000_022322c4.field_8 == 1)) {
            native_fn_02040564();
        }
        native_data_ov000_022322c4.field_8 = 0;
        native_fn_ov000_021e31a4();
    }
    return 0U;
}
