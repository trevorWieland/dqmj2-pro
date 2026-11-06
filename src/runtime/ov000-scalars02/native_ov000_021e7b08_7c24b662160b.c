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
extern u8 native_data_ov000_022351ec[];
u32 native_ov000_021e7b08(s32 arg0) {
    s32 var_r3;
    s32 var_r3_2;

    var_r3 = 0;
loop_1:
    if (arg0 == *(u32 *)(native_data_ov000_022351ec + (var_r3 * 4))) {
        return 0U;
    }
    var_r3 += 1;
    if (var_r3 >= 0x20) {
        var_r3_2 = 0;
loop_5:
        if (*(u32 *)(native_data_ov000_022351ec + (var_r3_2 * 4)) == 0) {
            *(u32 *)(native_data_ov000_022351ec + (var_r3_2 * 4)) = arg0;
            return 1U;
        }
        var_r3_2 += 1;
        if (var_r3_2 >= 0x20) {
            return 0U;
        }
        goto loop_5;
    }
    goto loop_1;
}
