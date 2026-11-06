#define NULL ((void *)0)
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
extern u8 native_data_ov001_022355ec[];
extern u8 native_data_ov001_022362ac[];
extern u8 native_data_ov001_02236f6c[];
extern u8 native_data_ov001_02237c2c[];
u32 native_ov001_021db438(s32 arg0, u32 arg1) {
    void *var_r2;

    var_r2 = NULL;
    if (arg1 < 3U) {
        if (arg0 == 0) {
            var_r2 = native_data_ov001_02236f6c + (arg1 * 0x440);
        }
        else if (arg0 == 1) {
            var_r2 = native_data_ov001_022362ac + (arg1 * 0x440);
        }
        else if (arg0 == 2) {
            var_r2 = native_data_ov001_022355ec + (arg1 * 0x440);
        }
        else if (arg0 == 3) {
            var_r2 = native_data_ov001_02237c2c + (arg1 * 0x440);
        }

    }
    return (u32) var_r2;
}
