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
extern u32 native_fn_020443ec();
extern u32 native_fn_0204458c();
extern u32 native_fn_ov001_0220b3e4();
extern u8 native_data_ov001_02239d04[];
void native_ov001_02203338(void) {
    s8 var_r4;
    u8 *var_r5;

    if (native_fn_020443ec() != 2) {
        return;
    }
    if (native_fn_0204458c() != 1) {
        return;
    }
    var_r5 = native_data_ov001_02239d04;
    var_r4 = 0;
    do {
        native_fn_ov001_0220b3e4(var_r4, M2C_FIELD(var_r5, s32 *, 0x1C), M2C_FIELD(var_r5, s32 *, 0x20), M2C_FIELD(var_r5, s32 *, 0x24));
        native_fn_ov001_0220b3e4(var_r4 + 2, M2C_FIELD(var_r5, s32 *, 0x28), M2C_FIELD(var_r5, s32 *, 0x2C), M2C_FIELD(var_r5, s32 *, 0x30));
        var_r4 += 1;
        var_r5 += 0x34;
    } while ((s32) var_r4 < 2);
}
