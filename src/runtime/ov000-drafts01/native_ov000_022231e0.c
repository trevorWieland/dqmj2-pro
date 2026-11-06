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
extern u32 native_fn_02041764();
extern u32 native_fn_ov000_02222a40();
extern u32 native_fn_ov000_02222ae8();
extern u32 native_fn_ov000_02222b7c();
extern u32 native_fn_ov000_02222c28();
extern u32 native_fn_ov000_02222c6c();
extern u32 native_fn_ov000_02222c90();
extern u32 native_fn_ov000_02222da8();
extern u32 native_fn_ov000_02222e7c();
extern u32 native_fn_ov000_02222e88();
extern u32 native_fn_ov000_02223068();
extern u32 native_fn_ov000_02223118();
extern u32 native_fn_ov000_02223190();
extern u8 native_data_ov000_02246574[];
u32 native_ov000_022231e0(void) {
    u32 var_r0;
    u32 var_r6;

    var_r0 = 1;
    var_r6 = 8;
    do {
        switch ((s8) *native_data_ov000_02246574) {
        default:
            break;
        case 0:
            var_r0 = native_fn_ov000_02222a40();
            break;
        case 1:
            var_r0 = native_fn_ov000_02222ae8();
            break;
        case 2:
            var_r0 = native_fn_ov000_02222b7c();
            break;
        case 3:
            var_r0 = native_fn_ov000_02222c28();
            break;
        case 4:
            var_r0 = native_fn_ov000_02222c6c();
            break;
        case 11:
            var_r6 = native_fn_ov000_02222c90();
            var_r0 = 0;
            break;
        case 5:
            var_r0 = native_fn_ov000_02222da8();
            break;
        case 6:
            var_r0 = native_fn_ov000_02222e7c();
            break;
        case 7:
            var_r0 = native_fn_ov000_02222e88();
            break;
        case 8:
            var_r0 = native_fn_ov000_02223068();
            break;
        case 9:
            var_r0 = native_fn_ov000_02223118();
            break;
        case 10:
            var_r0 = native_fn_ov000_02223190();
            break;
        }
    } while (var_r0 != 0);
    native_fn_02041764();
    return var_r6;
}
