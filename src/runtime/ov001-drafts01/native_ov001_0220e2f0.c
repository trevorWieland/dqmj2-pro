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
extern u32 native_fn_ov001_0220d838();
extern u32 native_fn_ov001_0220d888();
extern u32 native_fn_ov001_0220d8d0();
extern u32 native_fn_ov001_0220dac8();
extern u32 native_fn_ov001_0220db40();
extern u32 native_fn_ov001_0220de6c();
extern u32 native_fn_ov001_0220ded8();
extern u32 native_fn_ov001_0220e0c8();
extern u32 native_fn_ov001_0220e134();
extern u32 native_fn_ov001_0220e2e0();
typedef struct {
    u8 unknown_0[0x2];
    u8 field_2;
} Record_native_data_ov001_0223e0d8;
extern Record_native_data_ov001_0223e0d8 native_data_ov001_0223e0d8;
u32 native_ov001_0220e2f0(void) {
    u32 var_r0;
    u32 var_r7;

    var_r0 = 1;
    var_r7 = 0;
    do {
        switch (native_data_ov001_0223e0d8.field_2) {
        default:
            break;
        case 0:
            var_r0 = native_fn_ov001_0220d838();
            break;
        case 1:
            var_r0 = native_fn_ov001_0220d888();
            break;
        case 5:
            var_r0 = native_fn_ov001_0220d8d0();
            break;
        case 2:
            var_r0 = native_fn_ov001_0220dac8();
            break;
        case 6:
            var_r0 = native_fn_ov001_0220db40();
            break;
        case 3:
            var_r0 = native_fn_ov001_0220de6c();
            break;
        case 7:
            var_r0 = native_fn_ov001_0220ded8();
            break;
        case 4:
            var_r0 = native_fn_ov001_0220e0c8();
            break;
        case 8:
            var_r0 = native_fn_ov001_0220e134();
            break;
        case 9:
            native_fn_ov001_0220e2e0();
            var_r0 = 0;
            var_r7 = 1;
            break;
        }
    } while (var_r0 != 0);
    return var_r7;
}
