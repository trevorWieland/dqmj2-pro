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
extern u32 native_fn_ov001_0220b7b8();
extern u32 native_fn_ov001_0220b808();
extern u32 native_fn_ov001_0220b8fc();
extern u32 native_fn_ov001_0220bfc0();
extern u32 native_fn_ov001_0220c33c();
extern u32 native_fn_ov001_0220c554();
extern u32 native_fn_ov001_0220c888();
extern u32 native_fn_ov001_0220c9ec();
extern u32 native_fn_ov001_0220cbe4();
extern u32 native_fn_ov001_0220ce58();
extern u32 native_fn_ov001_0220cf8c();
extern u32 native_fn_ov001_0220d044();
extern u32 native_fn_ov001_0220d1f0();
extern u32 native_fn_ov001_0220d22c();
extern u32 native_fn_ov001_0220d260();
typedef struct {
    u8 unknown_0[0x3];
    u8 field_3;
} Record_native_data_ov001_0223e088;
extern Record_native_data_ov001_0223e088 native_data_ov001_0223e088;
u32 native_ov001_0220d278(void) {
    u32 var_r0;
    u32 var_r6;

    var_r0 = 1;
    var_r6 = 0;
    do {
        switch (native_data_ov001_0223e088.field_3) {
        default:
            break;
        case 0:
            var_r0 = native_fn_ov001_0220b7b8();
            break;
        case 1:
            var_r0 = native_fn_ov001_0220b808();
            break;
        case 2:
            var_r0 = native_fn_ov001_0220b8fc();
            break;
        case 3:
            var_r0 = native_fn_ov001_0220bfc0();
            break;
        case 6:
            var_r0 = native_fn_ov001_0220c33c();
            break;
        case 7:
            var_r0 = native_fn_ov001_0220c554();
            break;
        case 8:
            var_r0 = native_fn_ov001_0220c888();
            break;
        case 9:
            var_r0 = native_fn_ov001_0220c9ec();
            break;
        case 10:
            var_r0 = native_fn_ov001_0220cbe4();
            break;
        case 11:
            var_r0 = native_fn_ov001_0220ce58();
            break;
        case 12:
            var_r0 = native_fn_ov001_0220cf8c();
            break;
        case 13:
            var_r0 = native_fn_ov001_0220d044();
            break;
        case 14:
            var_r0 = native_fn_ov001_0220d1f0();
            break;
        case 5:
            var_r0 = native_fn_ov001_0220d22c();
            break;
        case 15:
            var_r0 = native_fn_ov001_0220d260();
            var_r6 = 1;
            break;
        }
    } while (var_r0 != 0);
    return var_r6;
}
