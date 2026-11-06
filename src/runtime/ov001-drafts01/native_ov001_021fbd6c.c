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
extern u32 native_fn_ov001_021f9608();
extern u32 native_fn_ov001_021f96b4();
extern u32 native_fn_ov001_021f98e4();
extern u32 native_fn_ov001_021f9b54();
extern u32 native_fn_ov001_021f9dc4();
extern u32 native_fn_ov001_021f9e10();
extern u32 native_fn_ov001_021fa06c();
extern u32 native_fn_ov001_021fa430();
extern u32 native_fn_ov001_021fa954();
extern u32 native_fn_ov001_021faaa0();
extern u32 native_fn_ov001_021fad50();
extern u32 native_fn_ov001_021fae50();
extern u32 native_fn_ov001_021fafec();
extern u32 native_fn_ov001_021fb7ac();
extern u32 native_fn_ov001_021fb960();
extern u32 native_fn_ov001_021fbce8();
extern u32 native_fn_ov001_021fbd50();
typedef struct {
    u8 unknown_0[0xa];
    u8 field_a;
} Record_native_data_ov001_02239a14;
extern Record_native_data_ov001_02239a14 native_data_ov001_02239a14;
u32 native_ov001_021fbd6c(void) {
    u32 var_r0;
    u32 var_r6;

    var_r0 = 1;
    var_r6 = 0;
    do {
        switch (native_data_ov001_02239a14.field_a) {
        default:
            break;
        case 0:
            var_r0 = native_fn_ov001_021f9608();
            break;
        case 1:
            var_r0 = native_fn_ov001_021f96b4();
            break;
        case 2:
            var_r0 = native_fn_ov001_021f98e4();
            break;
        case 3:
            var_r0 = native_fn_ov001_021f9b54();
            break;
        case 4:
            var_r0 = native_fn_ov001_021f9dc4();
            break;
        case 5:
            var_r0 = native_fn_ov001_021f9e10();
            break;
        case 6:
            var_r0 = native_fn_ov001_021fa06c();
            break;
        case 7:
            var_r0 = native_fn_ov001_021fa430();
            break;
        case 8:
            var_r0 = native_fn_ov001_021faaa0();
            break;
        case 9:
            var_r0 = native_fn_ov001_021fa954();
            break;
        case 10:
            var_r0 = native_fn_ov001_021fad50();
            break;
        case 11:
            var_r0 = native_fn_ov001_021fae50();
            break;
        case 12:
            var_r0 = native_fn_ov001_021fafec();
            break;
        case 13:
            var_r0 = native_fn_ov001_021fb7ac();
            break;
        case 14:
            var_r0 = native_fn_ov001_021fb960();
            break;
        case 15:
            var_r0 = native_fn_ov001_021fbce8();
            break;
        case 16:
            var_r0 = native_fn_ov001_021fbd50();
            var_r6 = 1;
            break;
        }
    } while (var_r0 != 0);
    return var_r6;
}
